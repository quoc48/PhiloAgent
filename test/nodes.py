

async def conversation_node(state: PhilosopherState, config: RunnableConfig):
    

async def conversation_node(state: PhilosopherState, config: RunnableConfig):
    summary = state.get("summary", "")
    conversation_chain = get_philosopher_response_chain()

    response = await conversation_chain.ainvoke(
        {
            "messages": state["messages"],
            "philosopher_context": state["philosopher_context"],
            "philosopher_name": state["philosopher_name"],
            "philosopher_perspective": state["philosopher_perspective"],
            "philosopher_style": state["philosopher_style"],
            "summary": summary,
        },
        config,
    )
    
    return {"messages": response}


def summarize_conversation_node():
    pass

def summarize_context_node():
    pass

def connector_node():
    pass    