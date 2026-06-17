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

**PolyDoc Chat** is a high-performance **Retrieval-Augmented Generation (RAG)** ecosystem designed to eliminate LLM hallucinations. By enforcing a strict verification protocol, it ensures that every AI-generated response is mathematically grounded in the provided technical documentation. It bridges the gap between massive document silos and actionable intelligence without compromising on data integrity or truth.

---

## ⚙️ How the RAG Pipeline Functions (Core Logic)

The system follows a sophisticated multi-stage pipeline to ensure data integrity and retrieval precision:

1.  **High-Speed Ingestion**: Documents are processed using asynchronous Python loaders. The system extracts text and metadata from formats like `PDF`, `DOCX`, `PPTX`, `CSV`, `Markdown`, and `TXT` while preserving structural hierarchy.
2.  **Neural Chunking & Semantic Partitioning**: Extracted text is divided into optimized "chunks" (semantic segments). This process ensures that context is maintained within each segment for better retrieval accuracy.
3.  **Local Embedding Generation**: Each chunk is transformed into a high-dimensional vector using the `sentence-transformers/all-MiniLM-L6-v2` model. This happens **locally** on your machine, ensuring metadata privacy.
4.  **Vector Store Orchestration (ChromaDB)**: These vectors are stored in a local **ChromaDB** instance with persistent storage capabilities. This allows for near-instant similarity searches when a user asks a query.
5.  **Context Injection & Prompt Engineering**: Upon a query, the most relevant chunks are retrieved and injected into a secure prompt. This prompt strictly instructs the LLM to only use the provided context.
6.  **Deterministic Synthesis**: The **Llama 3.3 70B** engine (via Groq API) synthesizes a response. If the answer is not present in the context, the system is hard-coded to report a lack of information rather than guessing.

---

## � Key Technical Features

- **Multi-Format Neural Mapping**: Parallel processing support for PDF, DOCX, PPTX, CSV, TXT, and Markdown.
- **Source-Grounded Attribution**: Every AI claim is backed by explicit citations, including the filename and exact page or slide number.
- **Deterministic Verification**: Hard-coded protocols to prevent hallucinations by restricting the model to provided context only.
- **High-Concurrency Indexing**: Asynchronous backend execution allows for parallel document indexing and high throughput.
- **Context Source Inspector**: A dedicated UI sheet to inspect the exact document segments utilized by the AI for any given response.

---

## �🛡️ Privacy & Security Architecture

> [!IMPORTANT]
> **Data Isolation Protocol**: Unlike standard AI tools, PolyDoc Chat generates embeddings locally. Your document's internal structure and metadata never leave your infrastructure. Only specific, encrypted text segments are sent to the inference engine during the final generation phase.

---

## 🎨 Industrial Design Philosophy

The interface is engineered with a **bespoke Industrial Cyber-Luxe Midnight Theme**, focusing on high-contrast readability and industrial precision.
- **Asymmetric Split Layout**: Strategically balances branding with technical utility to minimize cognitive load.
- **Cinematic Animations**: Framer Motion powered blur-transitions, neural pulses, and smooth state synchronizations.
- **Glassmorphism**: 100% pure-black backgrounds (`#020202`) with high-contrast emerald text and ambient glows.
- **Zero-Scroll Architecture**: Optimized ingestion and landing screens that fit perfectly within a single viewport.
- **Neural Field Interface**: A clean, high-fidelity chat interface with automatic smooth-scroll to the latest insights.

---

## 🛠 Technical Stack Details

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend** | React 18, TypeScript, Vite | For type-safety, lightning-fast HMR, and high-performance state management. |
| **Styling** | Tailwind CSS, Framer Motion | Utility-first approach for the Cyber-Luxe UI with cinematic animations. |
| **Backend** | FastAPI, Python 3.11 | Asynchronous REST API execution for high throughput and parallel processing. |
| **Inference** | Groq (Llama-3.3-70B) | Industry-leading inference speed (~200+ tokens/sec) and complex reasoning. |
| **Vector DB** | ChromaDB | Lightweight, local persistence with persistent vector search capabilities. |
| **Embeddings** | Sentence-Transformers | Local execution of `all-MiniLM-L6-v2` for maximum data privacy. |

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

## 📺 Video Demo (Technical Walkthrough)

> [!TIP]
> ### 🎥 Project Video Walkthrough
> **Watch the complete neural orchestration and system flow in this video demonstration:**
>
> <div align="center">
>   <a href="https://drive.google.com/file/d/1OC8cCQStC2aNMuUsHrMRrLizzVDsNH7d/view?usp=sharing" target="_blank">
>     <img src="https://img.shields.io/badge/CLICK_TO_WATCH-VIDEO_DEMO-RED?style=for-the-badge&logo=google-drive&logoColor=white" height="60px"/>
>   </a>
>   <br/>
>   <p style="margin-top: 15px;"><b>Click the badge above to watch the technical walkthrough on Google Drive</b></p>
> </div>

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

## Pipeline Methods & Evaluation Metrics

A detailed breakdown of every method used in the system and the evaluation metrics to measure performance:

### 1. Document Loaders (src_ai/loaders/document_loaders.py)
**Methods Implemented:**
- PDF Loading: PyMuPDF (fitz) + ThreadPoolExecutor (parallel page extraction)
- Table Loading: pandas for CSV/Excel files
- DOCX Loading: python-docx for Word documents
- PPTX Loading: python-pptx for PowerPoint slides
- TXT/Markdown: Standard file I/O

**Evaluation Metrics:**
| Metric | Description |
|--------|-------------|
| Text Extraction Accuracy | % of text correctly extracted compared to manual reference |
| Processing Speed | Time per document (seconds) |
| Parallel Efficiency | Speedup ratio with multi-threading vs single-thread |
| Metadata Preservation | % of page/slide/row numbers correctly captured |

---

### 2. Text Chunking
**Methods Implemented:**
- Algorithm: Recursive Character Text Splitter (LangChain)
- Chunk Size: 1000 characters
- Chunk Overlap: 100 characters
- Separators: `["\n\n", "\n", " ", ""]` (hierarchical splitting to preserve context)

**Evaluation Metrics:**
| Metric | Description |
|--------|-------------|
| Contextual Coherence | Semantic similarity between consecutive chunks |
| Retrieval Relevance | % of retrieved chunks that are relevant to queries |
| Chunk Size Consistency | Distribution uniformity of chunk sizes |
| Information Loss | % of key information preserved across splits |

---

### 3. Embedding Model (src_ai/models/embedder.py)
**Methods Implemented:**
- Model: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional vectors)
- Execution: Local (CPU/GPU) for data privacy
- Library: HuggingFace via LangChain

**Evaluation Metrics:**
| Metric | Description |
|--------|-------------|
| STS Score | Semantic Textual Similarity correlation with human judgment |
| Embedding Speed | Time per chunk (milliseconds) |
| Memory Usage | RAM consumed by model and embeddings |
| Recall@K | % of relevant chunks retrieved in top-K |

---

### 4. Vector Database (src_ai/retrievers/simple_retriever.py)
**Methods Implemented:**
- Vector DB: ChromaDB (lightweight, local persistence)
- Index Type: Flat Index (default for Chroma)
- Similarity: Cosine similarity
- Index Batching: 128 chunks per batch for parallel indexing

**Evaluation Metrics:**
| Metric | Description |
|--------|-------------|
| Query Latency | Time to retrieve top-K chunks (ms) |
| Indexing Throughput | Chunks indexed per second |
| NDCG | Normalized Discounted Cumulative Gain (ranks relevance) |
| Storage Size | Disk space used by vector index |

---

### 5. Retrieval System
**Methods Implemented:**
- Retrieval Type: Semantic similarity search
- Top-K: 8 chunks per query

**Evaluation Metrics:**
| Metric | Description |
|--------|-------------|
| Recall@1, 3, 5, 8 | % of relevant chunks found in top-N |
| Precision@1, 3, 5, 8 | % of top-N chunks that are relevant |
| F1-Score | Harmonic mean of precision and recall |
| MRR (Mean Reciprocal Rank) | Average reciprocal rank of first relevant chunk |
| MAP (Mean Average Precision) | Average precision across all queries |

---

### 6. RAG Service & LLM (src_ai/services/rag_service.py)
**Methods Implemented:**
- LLM: Llama 3.3 70B (Groq API)
- Temperature: 0.1 (low, for deterministic responses)
- Prompt Engineering: Strict context-only instructions to prevent hallucinations
- Conversation History: Optional multi-turn chat support

**Evaluation Metrics:**
| Metric | Description |
|--------|-------------|
| Answer Correctness | Human/LLM-as-a-judge evaluation |
| Answer Faithfulness | % of answer content supported by context (no hallucinations) |
| Answer Relevance | How relevant the answer is to the query |
| Generation Latency | Time to generate answer (seconds) |
| Citation Accuracy | % of citations correctly linked to context |
| Hallucination Rate | % of responses with unsupported information |

---

### 7. End-to-End System
**Evaluation Metrics:**
| Metric | Description |
|--------|-------------|
| E2E Latency | Total time from upload → query → answer |
| Throughput | Queries per second (QPS) |
| Error Rate | % of failed queries |

---

## Performance Benchmarks

Actual performance metrics from system evaluation (tested on local CPU):

### Document Loaders
| Metric | Value |
|--------|-------|
| Load time per document | 0.002 seconds |
| Throughput | 446,745 characters/second |
| Metadata preservation | 100% |

### Text Chunking
| Metric | Value |
|--------|-------|
| Chunking time per document | 0.0 seconds |
| Chunks created | 1 |
| Average chunk size | 883 characters |
| Chunking algorithm | RecursiveCharacterTextSplitter (1000 chars, 100 overlap) |

### Embedding Model
| Metric | Value |
|--------|-------|
| Embedding time per chunk | 0.1443 seconds |
| Embedding dimension | 384 |
| Model | sentence-transformers/all-MiniLM-L6-v2 |
| Device | CPU |

### Vector Database
| Metric | Value |
|--------|-------|
| Indexing time | 0.1027 seconds |
| Indexing throughput | 9.74 chunks/second |
| Similarity | Cosine Similarity |
| Vector DB | ChromaDB |

### Retrieval System
| Metric | Value |
|--------|-------|
| Average retrieval time | 16.6 ms |
| Minimum retrieval time | 14.16 ms |
| Maximum retrieval time | 19.78 ms |
| Top-K | 8 chunks |
| Retrieval type | Semantic Similarity Search |

### RAG Service
| Metric | Value |
|--------|-------|
| Average generation time | 0.5354 seconds |
| Minimum generation time | 0.3767 seconds |
| Maximum generation time | 0.6492 seconds |
| LLM | llama-3.3-70b-versatile (Groq) |
| Temperature | 0.1 |
| Answers with citations | 100% (4/4) |

### End-to-End System
| Metric | Value |
|--------|-------|
| Average E2E latency | 0.6948 seconds |
| Minimum E2E latency | 0.6222 seconds |
| Maximum E2E latency | 0.7454 seconds |

---

## Deployment & Local Setup

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

### 5. Running System Evaluation
Run the comprehensive evaluation module to measure performance of all pipeline components:
```bash
# From project root
python -m src_ai.evaluation
```
This will:
- Create a sample test document
- Evaluate document loaders, chunking, embeddings, retrieval, and RAG service
- Generate a detailed `evaluation_results.json` report
- Print a summary to the console

---
<div align="center">
  <b>PolyDoc Intelligent Core v1.0.4</b><br/>
  <i>Built for Precise Knowledge Retrieval • 2024</i>
</div>
