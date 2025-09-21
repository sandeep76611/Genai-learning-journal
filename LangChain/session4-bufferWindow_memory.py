from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key, temperature=0)

memory = ConversationBufferWindowMemory(k=4)  # remembers last 4 exchanges
conversation = ConversationChain(llm=llm, memory=memory)

print(conversation.predict(input="Hi my name is Sandeep!"))
print("=========================================")
print(conversation.predict(input="Tell me a joke"))
print("=========================================")
print(conversation.predict(input="What did I just ask?"))
