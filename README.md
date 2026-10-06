# Local RAG Hybrid Search

A local Retrieval-Augmented Generation (RAG) system that allows users to ask questions about their documents and receive answers based on the retrieved information.

The project combines **semantic search** with **keyword search (BM25)** to improve document retrieval, while running the AI components locally.

## Technologies

* **Python**
* **FastAPI** — Backend REST API
* **Streamlit** — Frontend interface
* **Qdrant** — Vector database
* **Sentence Transformers** — Text embeddings
* **BM25** — Keyword-based retrieval
* **Ollama** — Local LLM inference
* **PyTorch**
* **Docker** — Running Qdrant
* **Git & GitHub**

## Features

* 📄 Document ingestion and storage
* 🔎 Semantic vector search
* 🔤 Keyword search using BM25
* 🔀 Hybrid search combining semantic and keyword retrieval
* 🤖 Local LLM-based answer generation
* 💬 Conversational chat with session history
* 📚 Source-aware answers
* 🖥️ Streamlit interface
* ⚡ FastAPI backend
* 🐳 Qdrant running locally with Docker
* 🔒 Local processing without relying on a hosted RAG service

## The Process

The project was built step by step, starting from document processing and gradually integrating the different components of the RAG pipeline.

### 1. Document ingestion

Documents are loaded and processed into smaller text chunks.

Chunking makes it easier to retrieve only the relevant parts of a document instead of sending the entire document to the language model.

### 2. Generate embeddings

Each text chunk is converted into a vector representation using a sentence-transformer model.

These embeddings capture the semantic meaning of the text.

### 3. Store vectors in Qdrant

The generated embeddings and their associated text are stored in **Qdrant**, which is used as the vector database.

Qdrant runs locally through Docker.

### 4. Semantic search

When the user asks a question, the question is converted into an embedding.

Qdrant then searches for chunks that are semantically similar to the question.

### 5. Keyword search

A second retrieval method was implemented using **BM25**.

Unlike semantic search, BM25 focuses on keyword matching between the question and the document chunks.

### 6. Hybrid search

The results from semantic search and BM25 are combined to obtain more relevant documents.

This gives the system both:

* **Semantic understanding** — finding conceptually similar information
* **Keyword matching** — finding exact or important terms

### 7. Generate the answer

The retrieved chunks are provided to the local LLM together with the user's question.

The model generates an answer based on the retrieved context.

### 8. Conversation memory

A session ID is used to keep track of the conversation history, allowing the assistant to consider previous messages during the conversation.

### 9. Connect the components

Finally, the components were connected through a FastAPI backend and a Streamlit frontend.

The final architecture is approximately:


                 User
                  │
                  ▼
            Streamlit UI
                  │
                  ▼
             FastAPI API
                  │
                  ▼
           RAG Pipeline
            /         \
           ▼           ▼
    Hybrid Search   Chat History
       /      \
      ▼        ▼
 Qdrant       BM25
(Vector)    (Keyword)
      \        /
       ▼      ▼
       Retrieved Context
              │
              ▼
          Local LLM
              │
              ▼
            Answer


## What I Learned

Building this project helped me understand how a RAG system works beyond just using a framework or API.

### RAG fundamentals

I learned how the main components of a RAG pipeline work together:

**Documents → Chunking → Embeddings → Vector Database → Retrieval → Context → LLM → Answer**

### Vector databases

I learned how Qdrant stores embeddings and how vector similarity can be used to retrieve relevant information.

### Hybrid retrieval

I learned why combining different retrieval strategies can be useful.

Semantic search is good at understanding meaning, while BM25 can be better when exact keywords matter.

### Backend development

I learned how to build a REST API with FastAPI and connect the RAG pipeline to a frontend application.

### Local AI

I learned how to run LLM-based applications locally using Ollama instead of relying entirely on external APIs.

### Docker

I learned how Docker can be used to run infrastructure components such as Qdrant without installing and managing the database directly on the host system.

### Project structure

I also learned how to organize an AI application into separate components such as:

* API
* Retrieval
* Database
* RAG pipeline
* LLM
* Memory
* Frontend

## How to Run the Project

### Prerequisites

Make sure you have installed:

* Python
* Docker
* Ollama
* Git

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd local-rag-hybrid-search
```

### 2. Start Qdrant

Run Qdrant using Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

If you already have a Qdrant container configured for the project, start it with:

```bash
docker start <container_name>
```

### 3. Set up the backend

Open a terminal:

```powershell
cd backend
```

Create and activate the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Start the FastAPI server:

```powershell
uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

### 4. Set up the frontend

Open another terminal:

```powershell
cd frontend
```

Create and activate the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Run Streamlit:

```powershell
streamlit run app.py
```

The frontend will be available at:

```text
http://localhost:8501
```

### 5. Start Ollama

Make sure Ollama is running and that the model used by the project is available locally.

You can check your installed models with:

```powershell
ollama list
```

Then start the application and use the Streamlit interface to upload documents and ask questions.

---

## Project Structure

```text
local-rag-hybrid-search/
│
├── backend/
│   ├── api/
│   ├── db/
│   ├── retrieval/
│   ├── rag/
│   ├── llm/
│   ├── memory/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
