from langchain.memory import ConversationTokenBufferMemory
from langchain.chains import ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

# Store only last 100 tokens
memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=500)

conversation = ConversationChain(llm=llm, memory=memory,verbose=False)

print(conversation.predict(input="Hi, my name is Sandeep!"))
print(conversation.predict(input="What is my name?"))
print(conversation.predict(input="Tell me a joke"))
print(conversation.predict(input="Do you remember my name?"))

# View current memory variables
print(memory.load_memory_variables({}))