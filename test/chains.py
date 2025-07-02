

def get_chat_model(temperature: float = 0.7, model_name= str = settings.GROQ_LLM_MODEL) -> ChatGroq:
    
    from langchain.chat_models import ChatOpenAI

    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=model_name,
        temperature=temperature,
    )

def get_philosopher_response_chain():
     model = get_chat_model()
     model = model.bind_tools(tools)
     system_message = PHILOSOPHER_CHARACTER_CARD
     
     prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message.prompt),
            MessagesPlaceholder(variable_name="messages"),
        ],
        template_format="jinja2",
    )

    return prompt | model