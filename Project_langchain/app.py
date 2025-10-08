# app.py
import os
from typing import List, Dict, Any
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize LLM (Gemini for answers) + embeddings (HuggingFace local, free)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, api_key=API_KEY)
embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Session store
STORE: Dict[str, Any] = {"chunks": [], "embeddings": None}


def build_index(documents: List, chunk_size=1000, chunk_overlap=150):
    """Split docs into chunks, compute embeddings."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(documents)
    texts = [c.page_content for c in chunks]
    embeddings = np.array(embedder.embed_documents(texts))
    chunk_objs = [{"text": c.page_content, "metadata": c.metadata or {}, "id": i} for i, c in enumerate(chunks)]
    return chunk_objs, embeddings


def retrieve_top_k(query: str, embeddings: np.ndarray, chunks: List[Dict], top_k=4):
    """Retrieve top-k chunks."""
    if embeddings is None or not len(chunks):
        return []
    q_emb = np.array(embedder.embed_query(query))
    sims = cosine_similarity(q_emb.reshape(1, -1), embeddings).flatten()
    top_idx = sims.argsort()[::-1][:top_k]
    return [chunks[i] for i in top_idx]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    """Upload and process PDF/CSV into uploads/ folder."""
    suffix = os.path.splitext(file.filename)[1].lower()
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Load docs
    if suffix == ".pdf":
        docs = PyPDFLoader(file_path).load()
    elif suffix in [".csv", ".txt"]:
        docs = CSVLoader(file_path=file_path).load()
    else:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": f"Unsupported file type: {suffix}. Upload PDF or CSV."
        })

    # Build embeddings
    chunks, embeddings = build_index(docs)
    STORE.update({
        "chunks": chunks,
        "embeddings": embeddings,
        "file_name": file.filename,
        "file_type": suffix,
        "ready": True,
        "chat": []  # reset chat history
    })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "uploaded": True,
        "file_name": file.filename,
        "file_type": suffix,
        "chat": []
    })


@app.post("/ask", response_class=HTMLResponse)
async def ask(request: Request, question: str = Form(...)):
    """Answer questions in plain text like a bot."""
    if not STORE.get("ready"):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "No file uploaded yet.",
            "chat": []
        })

    retrieved = retrieve_top_k(question, STORE["embeddings"], STORE["chunks"], top_k=4)
    context = "\n\n".join([r["text"][:800] for r in retrieved])

    prompt = f"Answer based only on the context:\n\n{context}\n\nQuestion: {question}\nAnswer in plain text."
    llm_response = llm.invoke(prompt)
    answer = llm_response.content if llm_response and hasattr(llm_response, "content") else "No answer."

    # Append to chat history
    chat_entry = {"q": question, "a": answer}
    STORE["chat"].append(chat_entry)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "uploaded": True,
        "file_name": STORE.get("file_name"),
        "file_type": STORE.get("file_type"),
        "chat": STORE["chat"]
    })


@app.get("/health")
async def health():
    return {"status": "ok"}
