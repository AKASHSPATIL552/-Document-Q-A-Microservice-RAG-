from fastapi import FastAPI, UploadFile, File
from app.rag import ingest_document, answer_query
from app.database import init_db

app = FastAPI(title="RAG Document Q&A")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return await ingest_document(file)

from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query(request: QueryRequest):
    return answer_query(request.question)