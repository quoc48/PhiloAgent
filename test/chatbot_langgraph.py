from langgraph.graph import MessagesState

class PhilosopherState(MessagesState):
    summary: str

def create_simple_workflow_graph() -> StateGraph:
    graph_builder = StateGraph(PhilosopherState)

    # Add the essential nodes
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)
    
    # Define the simplied flow
    graph_builder.add_edge(START, "conversaton node")
    graph_builder.add_conditional_edges(
        "conversation_node",
        should_summarize_conversation,
    )
    graph_builder.add_edge("summarize_conversation_node", END)
    return graph_builder