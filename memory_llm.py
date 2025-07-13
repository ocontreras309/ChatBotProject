from langchain_openai import ChatOpenAI

from langchain_community.llms import OpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts.chat import MessagesPlaceholder

template = """
Eres un asistente virtual de nuestro instituto. Los clientes te harán preguntas sobre cursos y sus precios.\n\n

Ubicación del instituto: Av. América Este. Edificio Ferrara Piso 1 Oficina 2\n
Ciudad de Cochabamba, Bolivia\n
Precio del curso de Python: 200 Bs\n
Precio del curso de Robótica: 300 Bs\n

Inicio del curso de Python: 04 de septiembre\n
Inicio del curso de Robótica: 11 de septiembre\n
Sólo tenemos esos cursos por ahora\n
También vendemos kits de robótica educativa.\n

Si no conoces la respuesta, que manden un correo a info.cebtic@gmail.com

Conversación previa:
{historial}

Human: {pregunta}
Response:"""

llm = ChatOpenAI(temperature=1)

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            template
        ),
        MessagesPlaceholder(variable_name="historial"),
        HumanMessagePromptTemplate.from_template("{pregunta}")
    ]
)

memory = ConversationBufferMemory(memory_key="historial", return_messages=True)

conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
)

def store_conversation(text):
    return conversation({'pregunta': text})
