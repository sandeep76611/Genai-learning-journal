# import os 
# from dotenv import load_dotenv
# from langchain_experimental.text_splitter import SemanticChunker
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain.schema import Document


# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")   

# text = """
# AI in healthcare saves lives by detecting diseases early. It analyzes medical images and patient history. 
# In finance, AI detects fraud and improves customer service.
# """


# embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",google_api_key=api_key)
# semantic_splitter = SemanticChunker(embeddings)

# sematic_chunks = semantic_splitter.split_text(text)

# docs = [Document(page_content=chunk) for chunk in sematic_chunks]

# for i, doc in enumerate(docs, 1):
#     print(f"\nChunk {i} Content:", doc.page_content)
    
    
import os
from dotenv import load_dotenv
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Load your API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 1 Load the text file
text = """
Alice: Welcome everyone to the project kickoff meeting.
Bob: Our first agenda item is the budget and timeline.
Alice: Next, we’ll review the design prototypes and gather feedback.
Charlie: Finally, let’s assign tasks and plan the next steps.
Bob: Remember, the deadline is tight, so we need to prioritize features.
Alice: Agreed, we should focus on core functionalities first.
"""


# 2️ Create embeddings and semantic chunker
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key
)
semantic_splitter = SemanticChunker(embeddings)

# 3️ Split text semantically
semantic_chunks = semantic_splitter.split_text(text)

print("\nSplit text into semantic chunks:")
for i, c in enumerate(semantic_chunks, 1):
    print(f"\nChunk {i} preview:\n", c[:500], "...")  # first 500 chars

# 4️ Summarize each chunk using Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, api_key=api_key)

for i, c in enumerate(semantic_chunks, 1):
    summary = llm.invoke(
        f"Summarize this segment briefly in 3 bullet points and highlight key concepts:\n\n{c}"
    )
    print("\n---")
    print(f"Chunk {i} Summary:\n{summary.content}")
