import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


with open("sample.txt","r",encoding="utf-8") as file:
    text = file.read()


reader = PdfReader("sample.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"


char_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,       
    chunk_overlap=10,
    separators=["\n\n", "\n", " ", ""]
)

texts = char_splitter.split_text(text)

print(f"Number of chunks: {len(texts)}")
print("----------------------------------------------------------------")
print("First chunk preview:\n", texts[0])
print("----------------------------------------------------------------")
# --- 3. Summarize first chunk ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, api_key=api_key)
question = "Summarize this text:"
response = llm.invoke([HumanMessage(content=f"{question}\n\n{texts[0]}")])
print("Summary:", response.content)



