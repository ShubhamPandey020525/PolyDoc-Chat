from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant for a document-based question answering system. "
        "Answer ONLY using the provided context. "
        "If the answer is not present in the context, say: 'I don't know based on the given documents.' "
        "Do not make up information."
    ),
    (
        "human",
        "Context:\n{context}\n\nQuestion:\n{question}"
    )
])
