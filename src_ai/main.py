import asyncio
from src_ai.loaders.document_loaders import LoaderFactory
from src_ai.retrievers.hybrid_retriever import HybridRetriever
from src_ai.services.rag_service import GrokQueryEngine
from src_ai.core.logger import logger
from src_ai.core.config import settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

async def main():
    """Main entry point for PolyDoc-Chat Professional AI Core."""
    logger.info("Initializing PolyDoc-Chat Professional AI Core", 
                llm=settings.GROK_MODEL, 
                env=settings.ENVIRONMENT)
    
    # 1. Mock file path for testing (adjust if needed)
    test_file = "test_document.pdf" 
    if not os.path.exists(test_file):
        logger.warning(f"Test file {test_file} not found. Creating a mock for demo.")
        with open("test_document.txt", "w") as f:
            f.write("This is a professional document about PolyDoc-Chat AI. It uses Grok and hybrid retrieval.")
        test_file = "test_document.txt"

    # 2. Professional Loading & Splitting
    logger.info(f"Loading document: {test_file}")
    raw_docs = await LoaderFactory.load_async(test_file)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )
    
    # Chunking can be CPU bound, we could run in executor if many docs
    chunks = []
    for doc in raw_docs:
        split_texts = text_splitter.split_text(doc["content"])
        for text in split_texts:
            chunks.append({
                "content": text,
                "metadata": doc["metadata"]
            })

    # 3. Professional Indexing
    logger.info(f"Indexing {len(chunks)} chunks into vector store")
    hybrid_retriever = HybridRetriever()
    await hybrid_retriever.add_documents(chunks)
    
    # 4. Initialize Engine
    engine = GrokQueryEngine(retriever=hybrid_retriever)
    
    # 5. Execute Query
    query = "What is PolyDoc-Chat and how does it work?"
    logger.info("Running test query", query=query)
    
    try:
        result = await engine.process(query)
        
        print("\n" + "="*80)
        print("GROK ANALYSIS")
        print("="*80)
        print(result["answer"])
        print("\nSOURCES & CITATIONS")
        print("-" * 20)
        print(result["citations"])
        print("="*80)
    except Exception as e:
        logger.error("Failed to process query", error=str(e))

if __name__ == "__main__":
    asyncio.run(main())
