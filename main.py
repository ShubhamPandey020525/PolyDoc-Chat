import os
import uuid

from loaders import load_document
from chunker import chunk_text
from embedder import embed_text
from vectordb import upsert_vectors


DATA_DIR = "data"


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


def ingest_data_folder(base_dir):
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            ingest_file(file_path)


if __name__ == "__main__":
    ingest_data_folder(DATA_DIR)
