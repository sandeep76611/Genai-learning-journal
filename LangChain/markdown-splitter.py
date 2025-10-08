# from langchain.text_splitter import MarkdownHeaderTextSplitter


# markdown_document = """
# # Artificial Intelligence
# AI is transforming industries worldwide.

# ## Applications of AI
# ### Healthcare
# AI in healthcare saves lives by detecting diseases early.

# ### Finance
# AI improves fraud detection and customer service.

# # Ethical Concerns
# AI raises ethical issues like bias and job displacement.
# """

# headers_to_split_on = [("#","Header 1"), ("##","Header 2"), ("###","Header 3")]

# markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)


# header_chunks = markdown_splitter.split_text(markdown_document)

# print("----------------------------------------------------------------------")

# print(header_chunks)

# print("----------------------------------------------------------------------")

# for i, chunk in enumerate(header_chunks, 1):
#     print(f"\nChunk {i} Metadata:", chunk.metadata)
#     print("Content:", chunk.page_content)
    
    

from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 1. Pretend this is your blog post in Markdown
with open("sample.txt", "r", encoding="utf-8") as f:
    llm_text = f.read()

# 2. Split by headers
headers = [("#", "Header 1"), ("##", "Header 2")]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers)

sections = splitter.split_text(llm_text)


# 3. Summarize each section with an LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, api_key=api_key)

for idx, section in enumerate(sections, 1):
    doc = Document(page_content=section.page_content)
    header = section.metadata if section.metadata else {"Header": f"Untitled Section {idx}"}
    summary = llm.invoke(f"Summarize this section briefly:\n\n{doc.page_content}")
    print("----------------------------------------------------------------------")
    print("Header Metadata:", header)
    print("----------------------------------------------------------------------")
    print("Summary:", summary.content)


