import asyncio
from src_ai.loaders.document_loaders import LoaderFactory
from src_ai.retrievers.simple_retriever import SimpleRetriever
from src_ai.services.rag_service import GrokQueryEngine
from src_ai.core.logger import logger
from src_ai.core.config import settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

async def main():
    """Main entry point for PolyDoc-Chat AI Core."""
    logger.info("Initializing PolyDoc-Chat AI Core", 
                llm=settings.GROK_MODEL, 
                env=settings.ENVIRONMENT)
    
    # 1. Test file
    test_file = "test_document.txt"
    if not os.path.exists(test_file):
        with open(test_file, "w") as f:
            f.write("PolyDoc-Chat is a simple yet powerful RAG application. It supports multiple formats and uses Grok LLM.")
    
    # 2. Loading & Splitting
    logger.info(f"Loading document: {test_file}")
    raw_docs = await LoaderFactory.load_async(test_file)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )
    
    chunks = []
    for doc in raw_docs:
        split_texts = text_splitter.split_text(doc["content"])
        for text in split_texts:
            chunks.append({
                "content": text,
                "metadata": doc["metadata"]
            })

    # 3. Indexing
    logger.info(f"Indexing {len(chunks)} chunks")
    retriever = SimpleRetriever()
    await retriever.add_documents(chunks)
    
    # 4. Initialize Engine
    engine = GrokQueryEngine(retriever=retriever)
    
    # 5. Execute Query
    query = "What is PolyDoc-Chat?"
    logger.info("Running query", query=query)
    
    try:
        result = await engine.process(query)
        print("\n" + "="*50)
        print(f"ANSWER: {result['answer']}")
        print(f"SOURCES: {result['citations']}")
        print("="*50)
    except Exception as e:
        logger.error("Query failed", error=str(e))

if __name__ == "__main__":
    asyncio.run(main())
