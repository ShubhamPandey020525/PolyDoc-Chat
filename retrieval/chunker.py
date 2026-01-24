def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 150
):
    """
    Splits text into overlapping chunks to preserve context.

    Args:
        text (str): Input text
        chunk_size (int): Size of each chunk
        overlap (int): Overlap between consecutive chunks

    Returns:
        List[str]: List of text chunks
    """

    if not text or not text.strip():
        return []

    chunks = []
    text_length = len(text)
    start = 0

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap
        if start < 0:
            start = 0

    return chunks
