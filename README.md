# 🚀 PolyDoc Chat Professional
### AI-Powered Multi-Document RAG Chat System

<div align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"/>
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Search-yellow?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/xAI-Grok-black?style=for-the-badge"/>
</div>

<br/>

**PolyDoc Chat Professional** is a high-performance, full-stack RAG (Retrieval-Augmented Generation) system. It allows users to upload multiple documents and interact with them using advanced AI models like **xAI Grok** and **OpenAI**.

---

## 🌟 Key Features

✅ **Professional Tech Stack**: React + Vite + ShadcnUI frontend and FastAPI backend.
✅ **Hybrid Retrieval**: Combines semantic and keyword search for superior accuracy.
✅ **Advanced AI**: Integrated with **xAI Grok-1** for high-quality reasoning and responses.
✅ **Citations & Sources**: Every answer includes explicit source citations for transparency.
✅ **Multi-Format Support**: Process PDF, DOCX, TXT, CSV, and XLSX files.
✅ **Professional UI**: Modern, responsive dashboard with drag-and-drop uploads.

---

## 🧠 System Architecture

```text
User → React Frontend (Vite) → FastAPI Backend → AI Engine (src_ai)
                                                  ├── ChromaDB (Vector Search)
                                                  ├── Cohere (Reranking)
                                                  └── xAI Grok / OpenAI (LLM)
```

---

## 📂 Project Structure

```bash
PolyDoc-Chat/
├── src_frontend/     # React + TypeScript + Tailwind + ShadcnUI
│   ├── components/   # UI & Layout components
│   └── lib/          # API clients & Shared types
├── src_backend/      # FastAPI REST API
│   ├── api/          # Route handlers (upload, chat)
│   └── core/         # Config & Logging
├── src_ai/           # RAG Logic & AI Services
│   ├── retrievers/   # Hybrid search (ChromaDB)
│   ├── models/       # Embeddings & Rerankers
│   └── services/     # Grok Query Engine
├── chroma_db/        # Persistent vector database (local)
└── .env.example      # Environment template
```

---

## 🛠 Tech Stack

| Layer          | Technology                      |
| -------------- | ------------------------------- |
| **Frontend**   | React 18, Vite, TypeScript, ShadcnUI |
| **Backend**    | FastAPI, Pydantic, Uvicorn      |
| **AI Engine**  | LangChain, xAI (Grok), OpenAI   |
| **Vector DB**  | ChromaDB                        |
| **Reranker**   | Cohere (Rerank-English-v3.0)    |

---

## 🚀 Getting Started

### 1. Prerequisites
- Node.js (v18+)
- Python (3.10+)
- API Keys: xAI (Grok), OpenAI, and Cohere.

### 2. Environment Setup
Copy the template and add your keys:
```powershell
cp .env.example .env
```
Update `.env` with your `XAI_API_KEY`, `OPENAI_API_KEY`, and `COHERE_API_KEY`.

### 3. Backend Installation
```powershell
pip install -r requirements.txt
python -m src_backend.main
```

### 4. Frontend Installation
```powershell
cd src_frontend
npm install
npm run dev
```

---

## 📜 License & Usage

© 2026 PolyDoc Chat — All Rights Reserved

This project is for professional portfolio and demonstration purposes.

You may:
✔ View and learn from the code
✔ Use as a reference for RAG architecture

You may NOT:
❌ Redistribute or sell the code
❌ Use for commercial production without permission
❌ Claim ownership of the architecture

---
