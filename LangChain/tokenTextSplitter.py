import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain.text_splitter import TokenTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


reader = PdfReader("sample.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"


token_splitter = TokenTextSplitter(
    chunk_size=200,          # token-based size
    chunk_overlap=30,
    encoding_name="cl100k_base"
)

texts = token_splitter.split_text(text)

print(f"Number of chunks: {len(texts)}")
print("----------------------------------------------------------------")
print("First chunk preview:\n", texts[0][:300])
print("----------------------------------------------------------------")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, api_key=api_key)
question = "Summarize the projects mentioned in the document:"
response = llm.invoke([HumanMessage(content=f"{question}\n\n{texts}")])
print("Summary:", response.content)
