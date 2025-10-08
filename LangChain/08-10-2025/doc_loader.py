from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


from langchain_community.document_loaders import UnstructuredWordDocumentLoader
loader = UnstructuredWordDocumentLoader("Data Science.docx")
documents = loader.load()

# Combine all text from the DOCX file
all_docx_text = "\n".join([doc.page_content for doc in documents])

print("DOCX loaded successfully with", len(documents), "sections/chunks")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, api_key=api_key)

prompt = f"Summarize this Word document in clear bullet points:\n\n{all_docx_text}"
response = llm.invoke(prompt)

print("DOCX Summary:")
print(response.content)

print("-------------------------------------------------------------------------------")

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
split_docs = splitter.split_documents(documents)

print(f"Document split into {len(split_docs)} chunks for detailed analysis")

# If you want: summarize each chunk individually
for i, chunk in enumerate(split_docs[:3]):  # limit to first 3 chunks for demo
    chunk_response = llm.invoke(f"Summarize this section:\n{chunk.page_content}")
    print(f"\n🔹 Chunk {i+1} Summary:\n{chunk_response.content}")


# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# import os
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# docx_path = "document.docx"

# try:
#     from langchain_community.document_loaders import Docx2txtLoader
#     loader = Docx2txtLoader(docx_path)
#     print("✅ Using Docx2txtLoader")
# except ModuleNotFoundError:
#     from langchain_community.document_loaders import UnstructuredWordDocumentLoader
#     loader = UnstructuredWordDocumentLoader(docx_path)
#     print("⚙️ Falling back to UnstructuredWordDocumentLoader")

# documents = loader.load()
# all_docx_text = "\n".join([doc.page_content for doc in documents])

# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, api_key=api_key)
# response = llm.invoke("Summarize this Word document in bullet points:\n" + all_docx_text)

# print("\nDOCX Summary:\n", response.content)
