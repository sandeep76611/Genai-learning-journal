# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains import ConversationChain
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_community.memory.kg import ConversationKGMemory
# import time

# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")

# # LLM
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key, temperature=0)

# # Knowledge Graph Memory
# memory = ConversationKGMemory(llm=llm)

# conversation = ConversationChain(llm=llm, memory=memory)

# print(conversation.predict(input="Hi, I am Sandeep from India!"))
# print("=========================================")
# print(conversation.predict(input="I work on LangChain, Python and FastAPI"))
# print("=========================================")
# print(conversation.predict(input="Where am I from?"))

# print("=== Knowledge Graph Triples ===")
# print(memory.kg.get_triples())


# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq  # new import
# from langchain.chains import ConversationChain
# from langchain_community.memory.kg import ConversationKGMemory

# # Load .env variables
# load_dotenv()

# # Load Groq API Key
# groq_api_key = os.getenv("GROQ_API_KEY")

# # Groq LLM (example model: mixtral-8x7b or llama3-70b)
# llm = ChatGroq(
#     groq_api_key=groq_api_key,
#     model="llama-3.1-8b-instant",  # or another supported Groq model
#     temperature=0
# )

# # Knowledge Graph Memory
# memory = ConversationKGMemory(llm=llm)

# # Conversation Chain
# conversation = ConversationChain(llm=llm, memory=memory)

# # Test it
# print(conversation.predict(input="Hi, I am Sandeep from India!"))
# print("=========================================")
# print(conversation.predict(input="I work on LangChain, Python and FastAPI"))
# print("=========================================")
# print(conversation.predict(input="Where am I from?"))

# print("=== Knowledge Graph Triples ===")
# print(memory.kg.get_triples())



# import os
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains import ConversationChain
# from langchain.prompts import PromptTemplate
# from langchain_community.memory.kg import ConversationKGMemory

# # Load API key from .env
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# # === LLM ===
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     api_key=api_key,
#     temperature=0
# )

# # === Knowledge Graph Memory ===
# memory = ConversationKGMemory(llm=llm)

# # === Custom Prompt ===
# template = """You are a helpful AI assistant.
# You have access to a knowledge graph of the conversation. 
# Use it to answer the user's questions even if they don't repeat details.

# Knowledge Graph Triples:
# {history}

# Current input: {input}

# Answer based on the above given inputs:"""

# prompt = PromptTemplate(
#     input_variables=["history", "input"],
#     template=template
# )

# # === Conversation Chain with KG Memory ===
# conversation = ConversationChain(
#     llm=llm,
#     memory=memory,
#     prompt=prompt,
#     verbose=True
# )

# # === Test Conversation ===
# print(conversation.predict(input="Hi, I am Sandeep from India!"))
# print("=========================================")
# print(conversation.predict(input="I work on LangChain, Python and FastAPI"))
# print("=========================================")
# print(conversation.predict(input="Where am I from?"))

# # === See Knowledge Graph Triples ===
# print("\n=== Knowledge Graph Triples ===")
# print(memory.kg.get_triples())


import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationKGMemory

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key, temperature=0)

memory = ConversationKGMemory(llm=llm)

conversation = ConversationChain(llm=llm, memory=memory)


print(conversation.predict(input="hi, i am jerin from india!"))
print("=========================================")
print(conversation.predict(input="i work on langchain,python and fastapi?"))
print("=========================================")
print(conversation.predict(input="where i am from?"))
print("=========================================")
print(conversation.predict(input="what do i work on?"))
print("=========================================")
