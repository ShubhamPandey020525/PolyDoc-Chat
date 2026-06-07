# �️ PolyDoc Chat: Enterprise Document Intelligence

<div align="center">
  <img src="proofs/6.png" width="100%" alt="PolyDoc Chat Hero"/>
  <br/>
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"/>
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Search-yellow?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Llama_3.3-Groq_API-emerald?style=for-the-badge"/>
</div>

---

## 📺 Project Showcase

### 🎥 Video Demo
[**Watch the Full Demonstration on Google Drive**](https://drive.google.com/file/d/1OC8cCQStC2aNMuUsHrMRrLizzVDsNH7d/view?usp=sharing)

### 📸 Technical Interface
<div align="center">
  <p align="center">
    <b>Intelligence Session & Neural Attribution</b><br/>
    <img src="proofs/7.png" width="48%" />
    <img src="proofs/8.png" width="48%" />
  </p>
</div>

---

## 🌌 Overview

**PolyDoc Chat** is a high-performance **Retrieval-Augmented Generation (RAG)** ecosystem engineered for deterministic multi-format document analysis. Unlike generic chatbots, PolyDoc is built for **Precision Insight** and **Zero Hallucination**, ensuring every AI-generated response is strictly grounded in your private technical assets.

Designed with a **Cyber-Luxe Midnight UI**, the application provides a seamless, industrial-grade experience for knowledge workers and technical researchers.

---

## ⚡ Key Technical Features

### 🧠 Neural RAG Core
- **Deterministic Retrieval**: Leverages **ChromaDB** for local vector persistence, ensuring data never leaves your infrastructure during indexing.
- **Llama 3.3 70B Engine**: Powered by **Groq** for near-instant inference and complex reasoning over multi-page documents.
- **Neural Mapping**: Advanced document parsing for PDF, DOCX, PPTX, CSV, Markdown, and TXT.

### 🛡️ Privacy & Security
- **Data Isolation**: Local embedding generation using `sentence-transformers/all-MiniLM-L6-v2`.
- **Zero-Cloud Indexing**: Your document vectors are stored locally, providing an air-gap security feel for sensitive data.

### 🔍 Verified Attribution
- **Source Citations**: Every claim is backed by explicit citations (File name + Page/Slide number).
- **Neural Attribution Sheet**: A dedicated "Context Sources" viewer allows you to inspect the exact document segments used by the AI.

---

## 🎨 UI/UX: The Cyber-Luxe Interface

The application features a **bespoke Asymmetric Split Layout** designed to maximize efficiency and minimize cognitive load:
- **Cinematic Midnight Theme**: High-contrast, pure-black backgrounds (`#020202`) with emerald and blue ambient glows.
- **Deterministic Layout**: Single-page focus with zero scrollbars in the landing and ingestion phases.
- **Neural Transitions**: Smooth Framer Motion animations (Blur + Scale) between system states.

---

## 🛠 Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | React 18, Vite, TypeScript | High-performance, type-safe web core. |
| **Styling** | Tailwind CSS, Framer Motion | Cyber-luxe UI with cinematic animations. |
| **Backend** | FastAPI, Python 3.11 | Asynchronous REST API for high throughput. |
| **Vector DB** | ChromaDB | Local persistence for vector search. |
| **AI Generation**| Groq (Llama-3.3-70B) | State-of-the-art LLM for precise extraction. |
| **Embeddings** | Sentence Transformers | Efficient local vector generation. |

---

## 📂 Project Architecture

```bash
PolyDoc-Chat/
├── src_frontend/     # React Core (Cinematic UI)
│   ├── components/   # IngestionMode, IntelligenceSession, ChatField
│   └── lib/          # API Orchestration & Shared Schemas
├── src_backend/      # FastAPI Server (Neural Bridge)
│   ├── api/          # Endpoints for Upload & Intelligence
│   └── core/         # Server State & Security Config
├── src_ai/           # Intelligence Core (RAG Pipeline)
│   ├── loaders/      # Parallel multi-format document loaders
│   ├── retrievers/   # Similarity search (ChromaDB)
│   ├── models/       # Local Embedders
│   └── services/     # RAG Orchestration (Groq Integration)
├── chroma_db/        # Local Vector Persistence
└── .env              # Neural Core Configuration
```

---

## � Deployment & Setup

### 1. Environment Preparation
Ensure you have Python 3.11+ and Node.js 18+ installed.

### 2. Neural Core Configuration
Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Initialize Backend
```bash
pip install -r requirements.txt
python -m src_backend.main
```

### 4. Initialize Frontend
```bash
cd src_frontend
npm install
npm run dev
```

---

## � Developer Notes
PolyDoc Chat was built to solve the "Hallucination Problem" in enterprise documentation. By combining **Local Vector Search** with **Llama 3.3's 70B reasoning**, we provide a tool that doesn't just "chat"—it verifies.

---
<div align="center">
  <b>Built for the Modern Knowledge Worker</b><br/>
  <i>Protocol v1.0.4 • Deterministic Intelligence</i>
</div>
