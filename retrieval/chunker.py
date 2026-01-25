import re


def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 150
):
    """
    Sentence-aware chunking for better semantic retrieval.
    """

    if not text or not text.strip():
        return []

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)

        if current_length + sentence_length <= chunk_size:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            chunk = " ".join(current_chunk).strip()
            if chunk:
                chunks.append(chunk)

            # overlap handling
            overlap_text = " ".join(current_chunk)[-overlap:]
            current_chunk = [overlap_text, sentence]
            current_length = len(overlap_text) + sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk).strip())

    return chunks
