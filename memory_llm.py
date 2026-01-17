from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory

template = """
Eres un asistente virtual de nuestro instituto. Los clientes te harán preguntas sobre cursos y sus precios.

Ubicación del instituto: Av. América Este. Edificio Ferrara Piso 1 Oficina 2
Ciudad de Cochabamba, Bolivia
Precio del curso de Python: 200 Bs
Precio del curso de Robótica: 300 Bs

Inicio del curso de Python: 04 de septiembre
Inicio del curso de Robótica: 11 de septiembre
Sólo tenemos esos cursos por ahora
También vendemos kits de robótica educativa.

Si no conoces la respuesta, que manden un correo a info.cebtic@gmail.com
"""

llm = ChatOpenAI(temperature=1)

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("placeholder", "{chat_history}"),
    ("human", "{input}")
])

# Store history per session
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Simple chain without manual history handling
chain = prompt | llm

# Wrap with RunnableWithMessageHistory
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

def store_conversation(text):
    return chain_with_history.invoke(
        {'input': text},
        config={"configurable": {"session_id": "user123"}}
    )