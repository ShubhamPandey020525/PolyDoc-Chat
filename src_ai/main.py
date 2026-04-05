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
    
    # 3. Professional Indexing
    logger.info("Indexing chunks into vector store")
    hybrid_retriever = HybridRetriever()
    await hybrid_retriever.add_documents(chunks)
    
    # 5. Execute Query
    query = "What is the main finding of this document?"
    logger.info("Running test query", query=query)
    result = await engine.process(query)
    logger.info("Response received", answer=result["answer"])

if __name__ == "__main__":
    asyncio.run(main())    query = "Summarize the key findings of this report in professional detail."
    logger.info("Processing user query", query=query)
    
    result = engine.process(query)
    
    print("\n" + "="*80)
    print("GROK ANALYSIS")
    print("="*80)
    print(result["answer"])
    print("\nSOURCES & CITATIONS")
    print("-" * 20)
    print(result["citations"])
    print("="*80)

if __name__ == "__main__":
    main()
