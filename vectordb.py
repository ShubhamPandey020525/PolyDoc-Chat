import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

_PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
_PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")

if not _PINECONE_API_KEY or not _PINECONE_INDEX_NAME:
    raise RuntimeError("Pinecone API key or index name missing in environment variables")

_pc = Pinecone(api_key=_PINECONE_API_KEY)
_index = _pc.Index(_PINECONE_INDEX_NAME)


def upsert_vectors(vectors: list):
    """
    Stores vectors into Pinecone.

    Each vector item must have:
    {
        "id": str,
        "values": List[float],
        "metadata": dict
    }
    """

    if not vectors:
        return

    _index.upsert(vectors=vectors)


def semantic_search(query_vector: list, top_k: int = 5):
    """
    Performs semantic (vector similarity) search in Pinecone.

    Args:
        query_vector (List[float]): Embedded query
        top_k (int): Number of results

    Returns:
        List[dict]: Matched metadata entries
    """

    if not query_vector:
        return []

    result = _index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )

    return result.get("matches", [])
