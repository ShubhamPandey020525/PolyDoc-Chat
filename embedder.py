import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Cohere API key
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise RuntimeError("COHERE_API_KEY not found in .env file")

# Cohere embedding endpoint
COHERE_EMBED_URL = "https://api.cohere.ai/v1/embed"

# HTTP headers
HEADERS = {
    "Authorization": f"Bearer {COHERE_API_KEY}",
    "Content-Type": "application/json",
}

# =========================
# Embedding function
# =========================
def embed_text(text: str):
    """
    Takes a string and returns a vector embedding (list of floats)
    using Cohere embed-english-v3.0 model.
    """

    if not text or not text.strip():
        return None

    payload = {
        "model": "embed-english-v3.0",
        "texts": [text],
        "input_type": "search_document"
    }

    response = requests.post(
        COHERE_EMBED_URL,
        headers=HEADERS,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Cohere API error {response.status_code}: {response.text}"
        )

    data = response.json()

    # Cohere returns: { "embeddings": [[...vector...]] }
    embedding = data["embeddings"][0]

    return embedding
