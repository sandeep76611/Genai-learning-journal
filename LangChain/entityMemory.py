import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.memory import ConversationEntityMemory
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key, temperature=0)

# Memory
memory = ConversationEntityMemory(llm=llm)

# Prompt template (explicit history + input)
prompt = PromptTemplate(
    input_variables=["history", "input"],
    template="Conversation so far:\n{history}\nUser: {input}\nAI:"
)

# Chain
chain = LLMChain(llm=llm, prompt=prompt)

# Add session-aware history
chat_history = ChatMessageHistory()
conversation = RunnableWithMessageHistory(
    chain,
    lambda session_id: chat_history,
    input_messages_key="input",
    history_messages_key="history",
)

# Use it
print(conversation.invoke({"input": "Hi, i am Sandeep from india!"}, config={"configurable": {"session_id": "1"}}))
print("=========================================")
print(conversation.invoke({"input": "i work on langchain,python and fastapi?"}, config={"configurable": {"session_id": "1"}}))
print("=========================================")
print(conversation.invoke({"input": "can you repeat where i am from?"}, config={"configurable": {"session_id": "1"}}))
print("=========================================")
print(conversation.invoke({"input": "what do i work on?"}, config={"configurable": {"session_id": "1"}}))
print("=========================================")
print(conversation.invoke({"input": "where do i live?"}, config={"configurable": {"session_id": "1"}}))
print("=========================================")