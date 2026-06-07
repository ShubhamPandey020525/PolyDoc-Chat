# 🚀 PolyDoc Chat
### Production-Quality Multi-Document RAG Application

<div align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"/>
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Search-yellow?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/xAI-Grok--Beta-black?style=for-the-badge"/>
</div>

<br/>

**PolyDoc Chat** is a streamlined, high-performance RAG (Retrieval-Augmented Generation) system. It allows users to upload multiple documents and interact with them using **Groq (Llama-3.3-70B)**, ensuring answers are strictly based on the provided context.

---

## 🌟 Key Features

- ✅ **Multi-Format Support**: Upload and process PDF, DOCX, PPTX, CSV, TXT, and Markdown files.
- ✅ **Strict RAG Pipeline**: AI answers only using provided context, preventing hallucinations.
- ✅ **Multi-Document Chat**: Index multiple files at once and chat with your entire knowledge base.
- ✅ **Source Citations**: Every answer includes document names and relevant page/slide references.
- ✅ **Context Viewer**: Inspect the exact document chunks used by the AI to generate answers.
- ✅ **Persistent Index**: Locally stored ChromaDB ensures your data persists across restarts.

---

## 🧠 System Architecture

```text
User → React Frontend (Vite) → FastAPI Backend → AI Engine (src_ai)
                                                  ├── LoaderFactory (Multi-format)
                                                  ├── ChromaDB (Local Vector Store)
                                                  └── Groq (Llama-3.3-70B Generation)
```

---

## 📂 Project Structure

```bash
PolyDoc-Chat/
├── src_frontend/     # React + TypeScript + Tailwind + ShadcnUI
│   ├── components/   # UI components (UploadBox, ChatWindow, etc.)
│   └── lib/          # API services & Shared types
├── src_backend/      # FastAPI REST API
│   ├── api/          # Endpoints (upload, chat, clear)
│   └── core/         # Server state & Config
├── src_ai/           # RAG Core Logic
│   ├── loaders/      # Parallel multi-format document loaders
│   ├── retrievers/   # Similarity search (ChromaDB)
│   ├── models/       # OpenAI Embeddings
│   └── services/     # Grok RAG Engine
├── chroma_db/        # Persistent vector database
└── .env.example      # Optimized environment template
```

---

## 🛠 Tech Stack

| Layer          | Technology                      |
| -------------- | ------------------------------- |
| **Frontend**   | React 18, Vite, TypeScript, TailwindCSS |
| **Backend**    | FastAPI, Pydantic, Uvicorn      |
| **AI Engine**  | LangChain, Groq (Llama-3.3-70B), Local Embeddings |
| **Vector DB**  | ChromaDB (Local Persistence)    |
| **Parsing**    | PyMuPDF, python-docx, python-pptx, Markdown |

---

## 🚀 Getting Started

### 1. Prerequisites
- Node.js (v18+)
- Python (3.11+)
- API Keys: Groq (Llama-3.3-70B).

### 2. Environment Setup
Copy the template and add your keys:
```powershell
cp .env.example .env
```
Update `.env` with your `GROQ_API_KEY`.

### 3. Installation & Run

**Backend:**
```powershell
pip install -r requirements.txt
python -m src_backend.main
```

**Frontend:**
```powershell
cd src_frontend
npm install
npm run dev
```

---

## 📜 Usage Rules
- **Strict Context**: AI will clearly state if it cannot find the answer in the uploaded documents.
- **Local Data**: All document chunks and embeddings stay on your machine in the `chroma_db/` folder.
- **Reset**: Use the "Reset All" button in the UI to wipe the local database and start fresh.

---
© 2026 PolyDoc Chat
