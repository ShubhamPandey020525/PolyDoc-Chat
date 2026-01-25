import os
import uuid
import sys
import subprocess

from retrieval.loaders import load_document
from retrieval.chunker import chunk_text
from retrieval.embedder import embed_text
from retrieval.vectordb import upsert_vectors, semantic_search
from llm.rag_chain import run_rag


# =========================
# INGESTION
# =========================

def ingest_file(file_path):
    documents = load_document(file_path)
    vectors = []

    for doc in documents:
        text = doc["text"]
        metadata = doc["metadata"]

        chunks = chunk_text(text)

        for chunk in chunks:
            embedding = embed_text(chunk)

            if embedding is None:
                continue

            vectors.append({
                "id": str(uuid.uuid4()),
                "values": embedding,
                "metadata": {
                    **metadata,
                    "text": chunk
                }
            })

    if vectors:
        upsert_vectors(vectors)


def ingest_uploaded_file(file_bytes, filename):
    temp_path = f"temp_{filename}"

    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    ingest_file(temp_path)

    if os.path.exists(temp_path):
        os.remove(temp_path)


# =========================
# RAG QUERY
# =========================

def ask_question(question, top_k=10):
    query_vector = embed_text(question)

    if query_vector is None:
        return "Unable to process your question."

    retrieved_docs = semantic_search(query_vector, top_k=top_k)

    return run_rag(retrieved_docs, question)


# =========================
# UI LAUNCHER
# =========================

def run_ui():
    ui_path = os.path.join("ui", "ui.py")

    if not os.path.exists(ui_path):
        raise FileNotFoundError("ui/ui.py not found")

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", ui_path],
        check=True
    )


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    print("Starting PolyDoc Chat...")
    run_ui()
