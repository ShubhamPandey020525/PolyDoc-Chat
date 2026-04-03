from src_ai.loaders.document_loaders import LoaderFactory
from src_ai.retrievers.hybrid_retriever import HybridRetriever
from src_ai.services.rag_service import GrokQueryEngine
from src_ai.core.logger import logger
from src_ai.core.config import settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def main():
    """Main entry point for PolyDoc-Chat Professional AI Core."""
    logger.info("Initializing PolyDoc-Chat Professional AI Core", 
                llm=settings.GROK_MODEL, 
                env=settings.ENVIRONMENT)
    
    # 1. Load Data
    test_file = "sample_docs/test_report.pdf" 
    if not os.path.exists(test_file):
        logger.warning(f"Demo file not found at {test_file}. System initialized but waiting for data.")
        return
        
    logger.info("Loading document", file=test_file)
    raw_docs = LoaderFactory.load(test_file)
    
    # 2. Strategic Chunking
    logger.info("Applying strategic chunking", size=settings.CHUNK_SIZE, overlap=settings.CHUNK_OVERLAP)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
    )
    
    chunks = []
    for doc in raw_docs:
        texts = text_splitter.split_text(doc["content"])
        for text in texts:
            chunks.append({
                "content": text,
                "metadata": doc["metadata"]
            })
    
    # 3. Professional Indexing
    logger.info("Indexing chunks into vector store")
    hybrid_retriever = HybridRetriever()
    hybrid_retriever.add_documents(chunks)
    
    # 4. Engine Setup
    logger.info("Configuring Hybrid Retriever and Grok Query Engine")
    engine = GrokQueryEngine(hybrid_retriever)
    
    # 5. Execute Query
    query = "Summarize the key findings of this report in professional detail."
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
