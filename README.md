# -Document-Q-A-Microservice-RAG-

# RAG Document Q&A Microservice

A backend service that allows users to upload documents (PDF/TXT) and ask questions about them using Retrieval-Augmented Generation (RAG).


## 🏗️ Architecture Summary

The system consists of the following components:

1. **FastAPI Backend** - REST API with three main endpoints
2. **Document Processing** - Text extraction and chunking
3. **Vector Database (ChromaDB)** - Stores document embeddings for semantic search
4. **SQL Database (SQLite)** - Stores metadata (filename, chunk IDs, upload time)
5. **Embedding Model** - sentence-transformers (all-MiniLM-L6-v2)
6. **LLM Integration** - Groq API for answer generation

### Data Flow:
```
Upload → Extract Text → Chunk → Embed → Store in VectorDB & SQLite
Query → Embed Question → Semantic Search → Retrieve Context → LLM Generate Answer
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Groq API key (free from https://console.groq.com/keys)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the project root:
```
GROQ_API_KEY=your-groq-api-key-here
```

Or set directly in terminal:
```bash
# Windows PowerShell
$env:GROQ_API_KEY="your-groq-api-key-here"

# Linux/Mac
export GROQ_API_KEY="your-groq-api-key-here"
```

### 5. Run the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

## 📡 API Endpoints

### 1. Health Check
```bash
GET /health
```
**Response:**
```json
{
  "status": "healthy"
}
```

### 2. Upload Document
```bash
POST /upload
```
**Request:**
- Content-Type: `multipart/form-data`
- Body: file (PDF or TXT)

**Example using cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "status": "uploaded",
  "filename": "document.pdf",
  "chunks": 15
}
```

### 3. Query Document
```bash
POST /query
```
**Request:**
- Content-Type: `application/json`
- Body:
```json
{
  "question": "What is this document about?"
}
```

**Example using cURL:**
```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is this document about?\"}"
```

**Response:**
```json
{
  "question": "What is this document about?",
  "answer": "This document discusses..."
}
```

## 🧪 Testing the API

### Using Swagger UI (Recommended)
1. Navigate to: `http://127.0.0.1:8000/docs`
2. Use the interactive interface to test endpoints

### Using Postman
1. Import the API endpoints
2. Set Content-Type headers appropriately
3. Test each endpoint

### Using cURL
See examples in the API Endpoints section above.

## 📁 Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and endpoints
│   ├── rag.py               # RAG logic (ingest & query)
│   ├── llm.py               # LLM integration (Groq API)
│   ├── database.py          # SQLite database operations
│   └── utils.py             # Text extraction and chunking
├── data/
│   ├── uploads/             # Uploaded documents
│   └── chroma_db/           # ChromaDB persistent storage
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## 🔧 Technology Stack

- **Framework**: FastAPI 0.110.0
- **Server**: Uvicorn 0.27.1
- **Vector Database**: ChromaDB 0.4.24
- **SQL Database**: SQLite3 (built-in)
- **Embeddings**: sentence-transformers 2.6.1 (all-MiniLM-L6-v2)
- **LLM**: Groq API (llama-3.3-70b-versatile)
- **PDF Processing**: PyPDF2 3.0.1

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | API key for Groq LLM service | Yes |




## 👨‍💻 Author

**Akash S. Patil**
- Email: akashsp1928@gmail.com
- LinkedIn: [linkedin.com/in/akash-patil-135b4a288](https://www.linkedin.com/in/akash-patil-135b4a288)

## 📄 License

This project is created for the AI Engineer Round 1 Assignment.

---

**Note**: This project does not use any AI code-generation tools. All code is written manually with reference to official documentation.
