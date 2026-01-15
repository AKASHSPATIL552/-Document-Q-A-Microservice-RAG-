import os
import uuid
from datetime import datetime
from sentence_transformers import SentenceTransformer
import chromadb
from app.utils import extract_text, chunk_text
from app.database import insert_metadata
from app.llm import generate_answer

os.makedirs("data/uploads", exist_ok=True)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

chroma = chromadb.PersistentClient(path="data/chroma_db")

collection = chroma.get_or_create_collection("docs")


async def ingest_document(file):
    """
    Ingest a document: save file, extract text, chunk, embed, and store.
    """
    try:
        # Validate file type
        if not (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
            return {
                "status": "error",
                "message": "Only PDF and TXT files are supported"
            }
        
        path = f"data/uploads/{file.filename}"
        with open(path, "wb") as f:
            content = await file.read()
            if not content:
                return {
                    "status": "error",
                    "message": "Empty file uploaded"
                }
            f.write(content)

        text = extract_text(path)
        
        if not text or not text.strip():
            return {
                "status": "error",
                "message": "No text could be extracted from the document"
            }

        chunks = chunk_text(text)
        
        if not chunks:
            return {
                "status": "error",
                "message": "No valid chunks created from document"
            }

        upload_time = datetime.utcnow().isoformat()
        
        for chunk in chunks:
            cid = str(uuid.uuid4())
            embedding = embedder.encode(chunk).tolist()
            collection.add(
                ids=[cid],
                documents=[chunk],
                embeddings=[embedding]
            )
            insert_metadata(file.filename, cid, upload_time)

        return {
            "status": "uploaded",
            "filename": file.filename,
            "chunks": len(chunks)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Upload failed: {str(e)}"
        }


def answer_query(question):
    """
    Answer a question using RAG: retrieve relevant chunks and generate answer.
    """
    try:
        if not question or not question.strip():
            return {
                "status": "error",
                "message": "Question cannot be empty"
            }
        
        q_embed = embedder.encode(question).tolist()
        
        res = collection.query(
            query_embeddings=[q_embed],
            n_results=3
        )

        if not res["documents"] or not res["documents"][0]:
            return {
                "question": question,
                "answer": "No relevant documents found in the database. Please upload documents first.",
                "context": [],
                "status": "no_results"
            }

        context = "\n\n".join(res["documents"][0])
        
        answer = generate_answer(context, question)

        return {
            "question": question,
            "answer": answer,
            
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Query failed: {str(e)}",
            "question": question
        }