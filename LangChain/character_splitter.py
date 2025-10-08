from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import os 
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

with open("sample.txt", "r",encoding="utf-8") as file:
    text = file.read()
    
char_splitter = CharacterTextSplitter(separator="\n" ,chunk_size=200, chunk_overlap=10)
texts = char_splitter.split_text(text)

# print(f"Original text length: {texts}")
print(f"Original text : {texts}")

print("----------------------------------------------------------------")

print(f"First chunk text : {texts[0]}")

print("----------------------------------------------------------------")

print(f"Second chunk text : {texts[1]}")

print("----------------------------------------------------------------")

print(f"Number of chunks: {len(texts)}")

print("----------------------------------------------------------------")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=api_key)

question = "summarize this text"

message = HumanMessage(content=f"{question}\n\n{texts[0]}")

print(f"Invoking LLM... : {message.content}")

print("----------------------------------------------------------------")

response = llm.invoke([message])

print(f"Response: {response.content}")
