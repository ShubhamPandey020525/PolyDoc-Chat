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

## 🌌 Project Vision

**PolyDoc Chat** is a high-performance **Retrieval-Augmented Generation (RAG)** ecosystem designed to eliminate LLM hallucinations. By enforcing a strict verification protocol, it ensures that every AI-generated response is mathematically grounded in the provided technical documentation.

---

## ⚙️ How the RAG Pipeline Functions (Core Logic)

The system follows a sophisticated multi-stage pipeline to ensure data integrity and retrieval precision:

1.  **High-Speed Ingestion**: Documents are processed using asynchronous Python loaders. The system extracts text and metadata from formats like `PDF`, `DOCX`, and `CSV` while preserving structural hierarchy.
2.  **Neural Chunking & Semantic Partitioning**: Extracted text is divided into optimized "chunks." This process ensures that context is maintained within each segment for better retrieval accuracy.
3.  **Local Embedding Generation**: Each chunk is transformed into a high-dimensional vector using the `all-MiniLM-L6-v2` model. This happens **locally** on your machine, ensuring metadata privacy.
4.  **Vector Store Orchestration (ChromaDB)**: These vectors are stored in a local **ChromaDB** instance. This allows for near-instant similarity searches when a user asks a query.
5.  **Context Injection & Prompt Engineering**: Upon a query, the most relevant chunks are retrieved and injected into a secure prompt. This prompt strictly instructs the LLM to only use the provided context.
6.  **Deterministic Synthesis**: The **Llama 3.3 70B** engine (via Groq API) synthesizes a response. If the answer is not present in the context, the system is hard-coded to report a lack of information rather than guessing.

---

## 🛡️ Privacy & Security Architecture

> [!IMPORTANT]
> **Data Isolation Protocol**: Unlike standard AI tools, PolyDoc Chat generates embeddings locally. Your document's internal structure and metadata never leave your infrastructure. Only specific, encrypted text segments are sent to the inference engine during the final generation phase.

---

## 🎨 Industrial Design Philosophy

The interface is engineered with a **Cyber-Luxe Midnight Theme**, focusing on high-contrast readability and industrial precision.
- **Asymmetric Split Layout**: Strategically balances branding with technical utility.
- **Glassmorphism & Neural Pulses**: Uses Framer Motion for sophisticated state transitions.
- **Zero-Scroll Architecture**: Optimized ingestion screens that fit perfectly within a single viewport.

---

## 🛠 Technical Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend** | React 18, TypeScript, Vite | For type-safety and lightning-fast state synchronization. |
| **Backend** | FastAPI, Python 3.11 | High-concurrency processing for multi-document indexing. |
| **Inference** | Groq (Llama-3.3-70B) | Industry-leading speed and complex technical reasoning. |
| **Vector DB** | ChromaDB | Local persistence with persistent storage capabilities. |

---

## 📸 System Walkthrough & Technical Proofs

### 🖼️ Stage 1: Strategic Ingestion & Validation
<div align="center">
  <p><b>01. Protocol Landing Interface</b></p>
  <img src="proofs/1.png" width="100%" style="border-radius: 8px; border: 1px solid #333; margin-bottom: 20px;"/>
  
  <p><b>02. Neural Asset Ingestion Mode</b></p>
  <img src="proofs/2.png" width="100%" style="border-radius: 8px; border: 1px solid #333; margin-bottom: 20px;"/>
  
  <p><b>03. Multi-Format Support Verification</b></p>
  <img src="proofs/3.png" width="100%" style="border-radius: 8px; border: 1px solid #333; margin-bottom: 20px;"/>
  
  <p><b>04. Context Validation Logic</b></p>
  <img src="proofs/4.png" width="100%" style="border-radius: 8px; border: 1px solid #333; margin-bottom: 20px;"/>
  
  <p><b>05. Vector Space Mapping</b></p>
  <img src="proofs/5.png" width="100%" style="border-radius: 8px; border: 1px solid #333; margin-bottom: 20px;"/>
</div>

---

## 📺 Technical Demonstration

> [!TIP]
> ### 🎥 Project Video Walkthrough
> **Experience the full neural orchestration in action:**
>
> [![Watch Video](https://img.shields.io/badge/ACCESS_TECHNICAL_DEMO-RED?style=for-the-badge&logo=google-drive&logoColor=white)](https://drive.google.com/file/d/1OC8cCQStC2aNMuUsHrMRrLizzVDsNH7d/view?usp=sharing)
>
> *Click the badge above to open the Google Drive video demonstration.*

---

### 🚀 Stage 2: Intelligence Session (Neural Output)
<div align="center">
  <p><b>06. Deterministic Response Generation</b></p>
  <img src="proofs/6.png" width="100%" style="border-radius: 8px; border: 1px solid #333; margin-bottom: 20px;"/>
  
  <p><b>07. Source Attribution & Citations</b></p>
  <img src="proofs/7.png" width="100%" style="border-radius: 8px; border: 1px solid #333; margin-bottom: 20px;"/>
  
  <p><b>08. Technical Context Breakdown</b></p>
  <img src="proofs/8.png" width="100%" style="border-radius: 8px; border: 1px solid #333; margin-bottom: 20px;"/>
</div>

### 🧹 Stage 3: Maintenance & Reset
<div align="center">
  <p><b>09. Secure System Purge Protocol</b></p>
  <img src="proofs/9.png" width="100%" style="border-radius: 8px; border: 1px solid #333; margin-bottom: 20px;"/>
</div>

---

## 🚀 Deployment & Local Setup

Follow these steps to initialize the PolyDoc Intelligent Core on your local infrastructure:

### 1. Environment Preparation (Conda)
It is recommended to use a dedicated Conda environment to ensure dependency isolation.

```bash
# Create the neural environment
conda create -n polydoc python=3.11 -y

# Activate the environment
conda activate polydoc
```

### 2. Neural Core Configuration
Create a `.env` file in the root directory to store your API credentials:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Backend Initialization (Neural Bridge)
Install the Python dependencies and launch the FastAPI server.
```bash
# Install RAG and API dependencies
pip install -r requirements.txt

# Launch the neural backend
python -m src_backend.main
```

### 4. Frontend Initialization (Intelligence UI)
In a new terminal, install the React dependencies and start the development server.
```bash
# Navigate to frontend directory
cd src_frontend

# Install UI dependencies
npm install

# Launch the cinematic interface
npm run dev
```

---
<div align="center">
  <b>PolyDoc Intelligent Core v1.0.4</b><br/>
  <i>Built for Precise Knowledge Retrieval • 2024</i>
</div>
