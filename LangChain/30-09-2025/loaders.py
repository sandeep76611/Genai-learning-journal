# from langchain_community.document_loaders import PyPDFLoader
# from langchain_community.document_loaders.csv_loader import CSVLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# # from langchain_community.vectorestores import FAISS
# from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# # from langchain.chains import RetrievalQA
# import os
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# # Load PDF document
# pdf_path = "python.pdf" 

# loader = PyPDFLoader(pdf_path)
# documents = loader.load()
# # print(documents)
# print("-------------------------------------------------------------------------------")

# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, api_key=api_key)

# docs = documents[0].page_content

# response = llm.invoke("summarize this pdf and give me in 1 points?"+ documents[1].page_content)

# print("Response:", response.content)


# loader1=CSVLoader(file_path="customers-100.csv")

# docs1=loader1.load()
# print(docs1)

# print("-------------------------------------------------------------------------------")

# result = llm.invoke("summarize this csv file?"+ docs1[0].page_content)

# print("Result:", result.content)



from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Load PDF document (ALL PAGES)

pdf_path = "python.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# Join all PDF pages into one text
all_pdf_text = "\n".join([doc.page_content for doc in documents])

print("PDF loaded with", len(documents), "pages")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, api_key=api_key)

# Ask LLM to summarize the whole PDF
response = llm.invoke("Summarize this PDF in points:\n" + all_pdf_text)
print("PDF Summary:", response.content)

print("-------------------------------------------------------------------------------")

# Load CSV file (ALL ROWS)

loader1 = CSVLoader(file_path="customers-100.csv")
docs1 = loader1.load()

# Join all CSV rows into one text
all_csv_text = "\n".join([doc.page_content for doc in docs1])

print("CSV loaded with", len(docs1), "rows")

# Ask LLM to summarize the whole CSV
result = llm.invoke("Summarize this CSV file:\n" + all_csv_text)
print("CSV Summary:", result.content)
