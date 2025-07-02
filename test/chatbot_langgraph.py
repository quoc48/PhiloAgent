from typing import Literal
from dataclasses_json import config
from langgraph.graph import StateGraph, MessagesState, END

# Giả lập settings
class Settings:
    TOTAL_MESSAGES_AFTER_SUMMARY = 5
    TOTAL_MESSAGES_SUMMARY_TRIGGER = 10

settings = Settings()

class PhilosopherState(MessagesState):
    summary: str
    philosopher_name: str

# Giả lập các hàm phụ trợ
def get_philosopher_response_chain():
    async def chain(messages, summary):
        return messages + [{"role": "assistant", "content": "Response: I am a philosopher."}]
    return chain

def get_conversation_summary_chain(summary):
    async def chain(messages, philosopher_name, summary):
        return f"Summary for {philosopher_name}: {summary} + new chat"
    return chain

def create_simple_workflow_graph() -> StateGraph:
    graph_builder = StateGraph(PhilosopherState)

    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)
    
    graph_builder.add_edge("__start__", "conversation_node")
    graph_builder.add_conditional_edges(
        "conversation_node",
        should_summarize_conversation,
    )
    graph_builder.add_edge("summarize_conversation_node", END)
    
    return graph_builder

async def conversation_node(state: PhilosopherState) -> PhilosopherState:
    summary = state.get("summary", "")
    conversation_chain = get_philosopher_response_chain()
    response = await conversation_chain(messages=state["messages"], summary=summary)
    return {"messages": response}

async def summarize_conversation_node(state: PhilosopherState) -> PhilosopherState:
    summary = state.get("summary", "")
    summary_chain = get_conversation_summary_chain(summary)
    response = await summary_chain(
        messages=state["messages"],
        philosopher_name=state.get("philosopher_name", "unknown"),
        summary=summary,
    )
    remaining_messages = state["messages"][-settings.TOTAL_MESSAGES_AFTER_SUMMARY:] if len(state["messages"]) > settings.TOTAL_MESSAGES_AFTER_SUMMARY else state["messages"]
    return {"summary": response, "messages": remaining_messages}

def should_summarize_conversation(state: PhilosopherState) -> Literal["summarize_conversation_node", "__end__"]:
    messages = state["messages"]
    print(f"Checking messages length: {len(messages)}")  # Debug
    if len(messages) >= settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversation_node"
    return "__end__"

import asyncio
graph_builder = create_simple_workflow_graph()
graph = graph_builder.compile()

async def main():
    initial_messages = [
        {"role": "user", "content": "Hello"}, {"role": "user", "content": "How are you?"}, {"role": "user", "content": "Tell me more"},
        {"role": "user", "content": "What’s next?"}, {"role": "user", "content": "Great!"}, {"role": "user", "content": "More details?"},
        {"role": "user", "content": "Thanks!"}, {"role": "user", "content": "Continue?"}, {"role": "user", "content": "Awesome!"},
        {"role": "user", "content": "Last one?"}
    ]
    print("=== Initial Conversation ===")
    async for event in graph.astream({"messages": initial_messages, "philosopher_name": "Epicurus"}):
        for value in event.values():
            if "messages" in value:
                for message in value["messages"]:
                    if isinstance(message, dict):
                        print(message.get("content", "Unknown content"))
                    else:
                        print(message.content)  # For HumanMessage/AIMessage objects
            if "summary" in value:
                print("=== Summary ===")
                print(value["summary"])

if __name__ == "__main__":
    asyncio.run(main())