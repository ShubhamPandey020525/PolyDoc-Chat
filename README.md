# 🛡️ PolyDoc Chat: Enterprise-Grade Document Intelligence Ecosystem

<div align="center">
  <img src="https://img.shields.io/badge/React_18-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"/>
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Search-yellow?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Llama_3.3_70B-Groq_API-emerald?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white"/>
</div>

---

## 🌌 Project Vision: What is PolyDoc Chat?

**PolyDoc Chat** is not just another chatbot; it is a **Deterministic Knowledge Retrieval Engine**. In an era where LLMs often "hallucinate" (provide false information), PolyDoc Chat enforces a **Strict RAG (Retrieval-Augmented Generation) Protocol**. 

It allows researchers, engineers, and corporate teams to upload hundreds of pages of technical documentation and interact with them using **Llama 3.3 70B** intelligence, ensuring every answer is mathematically derived from the provided context—never from the model's training data alone.

---

## ⚡ Technical Depth & Core Logic

### 🧠 The RAG Pipeline (How it works)
1.  **Ingestion & Parsing**: Parallel processing of `PDF`, `DOCX`, `PPTX`, `CSV`, `Markdown`, and `TXT` using high-performance Python libraries.
2.  **Neural Chunking**: Documents are split into semantic segments to preserve context.
3.  **Local Embedding Generation**: Vectors are generated locally using `all-MiniLM-L6-v2`, ensuring that sensitive metadata never leaves your machine.
4.  **Vector Store Orchestration**: **ChromaDB** persists these vectors locally for near-instant similarity searches.
5.  **Context Injection**: The most relevant document segments are injected into the prompt of **Llama 3.3 70B** via the **Groq API** (Inference speed: ~200+ tokens/sec).
6.  **Deterministic Synthesis**: The model is strictly instructed to answer "I don't know" if the answer isn't in the provided segments, eliminating hallucinations.

### 🛡️ Privacy Architecture
- **Air-Gapped Embedding Logic**: Embeddings are calculated on-device.
- **Metadata Isolation**: Document names and page numbers are stored in a local SQLite-backed vector store.
- **Encrypted Transmission**: Only the relevant text chunks and the query are sent for generation, never the entire document.

---

## 🎨 UI/UX: Cyber-Luxe Midnight Design
The application features a **bespoke Industrial Design** built to minimize cognitive load while looking like a high-end technical terminal:
- **Asymmetric Layout**: Shifts the visual priority between branding and utility.
- **Cinematic Animations**: Framer Motion powered blur-transitions and neural pulses.
- **Glassmorphism**: 100% pure-black backgrounds (`#020202`) with high-contrast emerald text for maximum readability.

---

## 🛠 Tech Stack Details

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend** | React 18 (Vite) | Lightning-fast HMR and high-performance state management. |
| **Styles** | Tailwind CSS | Utility-first approach for the Cyber-Luxe UI. |
| **Backend** | FastAPI (Python) | Asynchronous execution for parallel document indexing. |
| **LLM Engine** | Groq (Llama-3.3-70B) | State-of-the-art inference speed and reasoning. |
| **Vector DB** | ChromaDB | Lightweight, persistent, and developer-friendly local DB. |
| **Embeddings** | Sentence-Transformers | Local execution for data privacy. |

---

## 📂 Project Architecture Flow

```text
[DOCUMENTS] --> [PARALLEL LOADER] --> [CHUNK GENERATOR] 
                                            |
                                            v
[USER QUERY] --> [EMBEDDING ENGINE] --> [VECTOR SEARCH (ChromaDB)]
                                            |
                                            v
[GROQ API] <--- [PROMPT ORCHESTRATOR] <--- [CONTEXT SEGMENTS]
    |
    +-----> [DETERMINISTIC RESPONSE] + [CITATIONS (Page #, File)]
```

---

## 🚀 Installation & Neural Core Setup

### 1. Requirements
- Python 3.11+
- Node.js 18+
- Groq API Key

### 2. Environment Config
Create a `.env` in the root:
```bash
GROQ_API_KEY=your_secure_key_here
```

### 3. Start Neural Backend
```bash
pip install -r requirements.txt
python -m src_backend.main
```

### 4. Start Intelligence Frontend
```bash
cd src_frontend
npm install
npm run dev
```

---

## 👤 Developer Notes
PolyDoc Chat is a solution for **Enterprise Trust**. It bridges the gap between massive document silos and actionable intelligence without compromising on data integrity or truth.

---

## 📺 Project Showcase & Technical Proofs

### 🎥 Executive Video Demo
[**Watch the High-Definition Technical Demonstration**](https://drive.google.com/file/d/1OC8cCQStC2aNMuUsHrMRrLizzVDsNH7d/view?usp=sharing)

### 🖼️ System Gallery (Proof of Ingestion & Processing)

<div align="center">
  <table>
    <tr>
      <td width="50%"><b>01. Landing Architecture</b><br/><img src="proofs/1.png" width="100%"/></td>
      <td width="50%"><b>02. Neural Ingestion UI</b><br/><img src="proofs/2.png" width="100%"/></td>
    </tr>
    <tr>
      <td width="50%"><b>03. Multi-Format Support</b><br/><img src="proofs/3.png" width="100%"/></td>
      <td width="50%"><b>04. File Validation Logic</b><br/><img src="proofs/4.png" width="100%"/></td>
    </tr>
    <tr>
      <td width="50%"><b>05. Vector Indexing Process</b><br/><img src="proofs/5.png" width="100%"/></td>
      <td width="50%"><b>09. System Reset Protocol</b><br/><img src="proofs/9.png" width="100%"/></td>
    </tr>
  </table>
</div>

### 🚀 Neural Core Outputs (RAG Verification)
<div align="center">
  <p><b>High-Fidelity Response Generation with Source Attribution</b></p>
  <div style="display: flex; flex-direction: column; gap: 10px;">
    <img src="proofs/6.png" width="100%" />
    <div style="display: flex; gap: 10px;">
      <img src="proofs/7.png" width="49%"/>
      <img src="proofs/8.png" width="49%"/>
    </div>
  </div>
</div>

---
<div align="center">
  <b>Built for the Modern Knowledge Worker</b><br/>
  <i>Protocol v1.0.4 • High-Fidelity Intelligence • Deterministic Retrieval</i>
</div>
