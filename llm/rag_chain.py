from llm.llm_client import llm
from llm.prompt import RAG_PROMPT


def format_docs(retrieved_docs):
    """
    Converts retrieved Pinecone results into a single context string.
    """

    context_chunks = []

    for doc in retrieved_docs:
        metadata = doc.get("metadata", {})

        text = metadata.get("text")
        source = metadata.get("source", "unknown")

        if text:
            chunk = f"[Source: {source}]\n{text}"
            context_chunks.append(chunk)

    return "\n\n".join(context_chunks)


def run_rag(retrieved_docs, question):
    """
    Runs RAG: context + question → LLM → answer
    """

    context = format_docs(retrieved_docs)

    messages = RAG_PROMPT.format_messages(
        context=context,
        question=question
    )

    response = llm.invoke(messages)

    return response.content
