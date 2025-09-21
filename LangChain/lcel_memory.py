import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.9,
    api_key=api_key
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

parser = StrOutputParser()

chain = prompt | llm | parser

def run_conversation(user_input):
    history = memory.load_memory_variables({})["chat_history"]

    response = chain.invoke({
        "input": user_input,
        "chat_history": history
    })

    memory.save_context(
        {"input": user_input},
        {"output": response}
    )

    return response

print("A:", run_conversation("Hi! My name is Sandeep from India."))
print("B:",run_conversation("I work on LangChain, Python and FastAPI."))
print("C:",run_conversation("Can you repeat where I am from?"))
print("D:",run_conversation("What do I work on?"))
