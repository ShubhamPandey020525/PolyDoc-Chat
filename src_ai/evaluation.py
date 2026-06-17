"""
PolyDoc Chat: Evaluation Module
Comprehensive evaluation of all RAG pipeline components
"""

import os
import sys
import time
import json
import asyncio
from typing import List, Dict, Any, Optional

# Add project root to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src_ai.loaders.document_loaders import LoaderFactory
from src_ai.models.embedder import Embedder
from src_ai.retrievers.simple_retriever import SimpleRetriever
from src_ai.services.rag_service import GrokQueryEngine
from src_ai.core.config import settings
from src_ai.core.logger import logger
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PolyDocEvaluator:
    """
    Comprehensive evaluator for PolyDoc Chat RAG system
    """

    def __init__(self, test_dir: str = "test_data"):
        self.test_dir = test_dir
        os.makedirs(test_dir, exist_ok=True)

        # Initialize components
        self.embedder = Embedder()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )

        # Create a temporary retriever for testing
        self.temp_db_path = os.path.join(test_dir, "temp_chroma")
        self.retriever = SimpleRetriever(persist_directory=self.temp_db_path)

        # Results storage
        self.results: Dict[str, Any] = {
            "document_loaders": {},
            "chunking": {},
            "embeddings": {},
            "retrieval": {},
            "vector_db": {},
            "rag_service": {},
            "end_to_end": {}
        }

    async def create_sample_document(self) -> str:
        """Create a sample test document for evaluation"""
        sample_path = os.path.join(self.test_dir, "sample_doc.txt")
        sample_content = """
PolyDoc Chat is an enterprise-grade Retrieval-Augmented Generation system.
It was developed to eliminate LLM hallucinations through strict verification protocols.

Key Features:
1. Multi-format document support: PDF, DOCX, PPTX, CSV, TXT, Markdown
2. Local embedding generation using sentence-transformers/all-MiniLM-L6-v2
3. ChromaDB for persistent vector storage
4. Llama 3.3 70B via Groq API for fast inference
5. Source-grounded attribution with page/slide number citations

Technical Stack:
- Backend: FastAPI, Python 3.11
- Frontend: React 18, TypeScript, Tailwind CSS
- Vector DB: ChromaDB
- Embeddings: Sentence-Transformers
- LLM: Llama 3.3 70B (Groq)

Performance Highlights:
- Parallel PDF processing using ThreadPoolExecutor
- Recursive character text splitting with 1000-character chunks
- 8 chunks retrieved per query
- Low temperature (0.1) for deterministic responses
        """
        with open(sample_path, "w", encoding="utf-8") as f:
            f.write(sample_content)
        return sample_path

    async def evaluate_document_loaders(self, file_path: str):
        """Evaluate document loading performance"""
        logger.info("Evaluating document loaders...")
        start_time = time.time()

        try:
            docs = await LoaderFactory.load_async(file_path)
            load_time = time.time() - start_time

            total_chars = sum(len(doc["content"]) for doc in docs)
            num_pages = len(docs)

            self.results["document_loaders"] = {
                "status": "success",
                "load_time_seconds": round(load_time, 4),
                "num_documents_loaded": num_pages,
                "total_characters_extracted": total_chars,
                "metadata_preserved": all("source" in doc["metadata"] for doc in docs),
                "chars_per_second": round(total_chars / load_time if load_time > 0 else 0, 2)
            }

            logger.info(f"Document loader evaluation complete: {load_time:.4f}s")
            return docs

        except Exception as e:
            self.results["document_loaders"] = {
                "status": "failed",
                "error": str(e)
            }
            logger.error(f"Document loader evaluation failed: {str(e)}")
            return []

    def evaluate_chunking(self, docs: List[Dict[str, Any]]):
        """Evaluate text chunking performance"""
        logger.info("Evaluating text chunking...")
        start_time = time.time()

        try:
            all_chunks = []
            for doc in docs:
                split_texts = self.text_splitter.split_text(doc["content"])
                for text in split_texts:
                    all_chunks.append({
                        "content": text,
                        "metadata": doc["metadata"]
                    })

            chunk_time = time.time() - start_time

            chunk_sizes = [len(c["content"]) for c in all_chunks]
            avg_chunk_size = sum(chunk_sizes) / len(chunk_sizes) if chunk_sizes else 0
            min_chunk_size = min(chunk_sizes) if chunk_sizes else 0
            max_chunk_size = max(chunk_sizes) if chunk_sizes else 0

            self.results["chunking"] = {
                "status": "success",
                "chunking_time_seconds": round(chunk_time, 4),
                "num_chunks": len(all_chunks),
                "avg_chunk_size_chars": round(avg_chunk_size, 2),
                "min_chunk_size_chars": min_chunk_size,
                "max_chunk_size_chars": max_chunk_size,
                "chunk_size_range": max_chunk_size - min_chunk_size,
                "chunking_algorithm": "RecursiveCharacterTextSplitter",
                "chunk_size_config": settings.CHUNK_SIZE,
                "chunk_overlap_config": settings.CHUNK_OVERLAP
            }

            logger.info(f"Chunking evaluation complete: {chunk_time:.4f}s, {len(all_chunks)} chunks")
            return all_chunks

        except Exception as e:
            self.results["chunking"] = {
                "status": "failed",
                "error": str(e)
            }
            logger.error(f"Chunking evaluation failed: {str(e)}")
            return []

    def evaluate_embeddings(self, chunks: List[Dict[str, Any]]):
        """Evaluate embedding performance"""
        logger.info("Evaluating embeddings...")
        start_time = time.time()

        try:
            texts = [c["content"] for c in chunks]
            embeddings = self.embedder.embeddings.embed_documents(texts)
            embed_time = time.time() - start_time

            self.results["embeddings"] = {
                "status": "success",
                "embedding_time_seconds": round(embed_time, 4),
                "num_embeddings": len(embeddings),
                "embedding_dimension": len(embeddings[0]) if embeddings else 0,
                "model_used": settings.EMBEDDING_MODEL,
                "embeddings_per_second": round(len(embeddings) / embed_time if embed_time > 0 else 0, 2),
                "execution_device": "CPU"
            }

            logger.info(f"Embedding evaluation complete: {embed_time:.4f}s, {len(embeddings)} embeddings")
            return chunks

        except Exception as e:
            self.results["embeddings"] = {
                "status": "failed",
                "error": str(e)
            }
            logger.error(f"Embedding evaluation failed: {str(e)}")
            return []

    async def evaluate_vector_db_and_retrieval(self, chunks: List[Dict[str, Any]], test_queries: List[str]):
        """Evaluate vector DB and retrieval performance"""
        logger.info("Evaluating vector DB and retrieval...")

        try:
            # Indexing
            index_start = time.time()
            await self.retriever.add_documents(chunks)
            index_time = time.time() - index_start

            self.results["vector_db"] = {
                "status": "success",
                "indexing_time_seconds": round(index_time, 4),
                "num_chunks_indexed": len(chunks),
                "chunks_per_second": round(len(chunks) / index_time if index_time > 0 else 0, 2),
                "vector_db_used": "ChromaDB",
                "similarity_metric": "Cosine Similarity",
                "index_batch_size": settings.INDEX_BATCH_SIZE
            }

            # Retrieval
            retrieval_times = []
            all_retrieved_docs = []

            for query in test_queries:
                ret_start = time.time()
                docs = await self.retriever.search(query, top_k=settings.RETRIEVAL_TOP_K)
                ret_time = time.time() - ret_start
                retrieval_times.append(ret_time)
                all_retrieved_docs.append(docs)

            avg_retrieval_time = sum(retrieval_times) / len(retrieval_times) if retrieval_times else 0

            self.results["retrieval"] = {
                "status": "success",
                "num_test_queries": len(test_queries),
                "avg_retrieval_time_ms": round(avg_retrieval_time * 1000, 2),
                "min_retrieval_time_ms": round(min(retrieval_times) * 1000, 2) if retrieval_times else 0,
                "max_retrieval_time_ms": round(max(retrieval_times) * 1000, 2) if retrieval_times else 0,
                "top_k_config": settings.RETRIEVAL_TOP_K,
                "retrieval_type": "Semantic Similarity Search"
            }

            logger.info(f"Vector DB & retrieval evaluation complete")
            return all_retrieved_docs

        except Exception as e:
            self.results["vector_db"] = {
                "status": "failed",
                "error": str(e)
            }
            self.results["retrieval"] = {
                "status": "failed",
                "error": str(e)
            }
            logger.error(f"Vector DB & retrieval evaluation failed: {str(e)}")
            return []

    async def evaluate_rag_service(self, test_queries: List[str]):
        """Evaluate RAG service performance"""
        logger.info("Evaluating RAG service...")

        try:
            engine = GrokQueryEngine(retriever=self.retriever)
            generation_times = []
            answers = []

            for query in test_queries:
                gen_start = time.time()
                result = await engine.process(query)
                gen_time = time.time() - gen_start
                generation_times.append(gen_time)
                answers.append(result)

            avg_generation_time = sum(generation_times) / len(generation_times) if generation_times else 0

            self.results["rag_service"] = {
                "status": "success",
                "num_test_queries": len(test_queries),
                "avg_generation_time_seconds": round(avg_generation_time, 4),
                "min_generation_time_seconds": round(min(generation_times), 4) if generation_times else 0,
                "max_generation_time_seconds": round(max(generation_times), 4) if generation_times else 0,
                "llm_used": settings.GROQ_MODEL,
                "temperature": 0.1,
                "answers_with_citations": sum(1 for a in answers if a["citations"].strip())
            }

            logger.info(f"RAG service evaluation complete")
            return answers

        except Exception as e:
            self.results["rag_service"] = {
                "status": "failed",
                "error": str(e)
            }
            logger.error(f"RAG service evaluation failed: {str(e)}")
            return []

    async def evaluate_end_to_end(self, file_path: str, test_queries: List[str]):
        """Evaluate end-to-end system performance"""
        logger.info("Evaluating end-to-end system...")

        try:
            e2e_times = []

            for query in test_queries:
                e2e_start = time.time()

                # Full pipeline simulation
                docs = await LoaderFactory.load_async(file_path)
                all_chunks = []
                for doc in docs:
                    split_texts = self.text_splitter.split_text(doc["content"])
                    for text in split_texts:
                        all_chunks.append({
                            "content": text,
                            "metadata": doc["metadata"]
                        })

                await self.retriever.add_documents(all_chunks)
                engine = GrokQueryEngine(retriever=self.retriever)
                await engine.process(query)

                e2e_time = time.time() - e2e_start
                e2e_times.append(e2e_time)

            avg_e2e_time = sum(e2e_times) / len(e2e_times) if e2e_times else 0

            self.results["end_to_end"] = {
                "status": "success",
                "num_test_queries": len(test_queries),
                "avg_e2e_time_seconds": round(avg_e2e_time, 4),
                "min_e2e_time_seconds": round(min(e2e_times), 4) if e2e_times else 0,
                "max_e2e_time_seconds": round(max(e2e_times), 4) if e2e_times else 0
            }

            logger.info(f"End-to-end evaluation complete")

        except Exception as e:
            self.results["end_to_end"] = {
                "status": "failed",
                "error": str(e)
            }
            logger.error(f"End-to-end evaluation failed: {str(e)}")

    def save_results(self, output_path: str = "evaluation_results.json"):
        """Save evaluation results to JSON file"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)
        logger.info(f"Evaluation results saved to {output_path}")

    def print_summary(self):
        """Print a summary of evaluation results"""
        print("\n" + "="*80)
        print("POLYDOC CHAT: EVALUATION SUMMARY")
        print("="*80)

        for component, data in self.results.items():
            print(f"\n--- {component.upper()} ---")
            if data.get("status") == "success":
                for key, value in data.items():
                    if key != "status":
                        print(f"  {key}: {value}")
            else:
                print(f"  FAILED: {data.get('error', 'Unknown error')}")

        print("\n" + "="*80)

    async def run_full_evaluation(self):
        """Run complete evaluation pipeline"""
        logger.info("Starting full PolyDoc Chat evaluation...")

        # Create sample document
        sample_file = await self.create_sample_document()

        # Test queries
        test_queries = [
            "What is PolyDoc Chat?",
            "What embedding model is used?",
            "What LLM is used for generation?",
            "What are the key features of PolyDoc Chat?"
        ]

        # 1. Evaluate loaders
        docs = await self.evaluate_document_loaders(sample_file)
        if not docs:
            logger.warning("No documents loaded, skipping remaining steps")
            return

        # 2. Evaluate chunking
        chunks = self.evaluate_chunking(docs)
        if not chunks:
            logger.warning("No chunks created, skipping remaining steps")
            return

        # 3. Evaluate embeddings
        chunks = self.evaluate_embeddings(chunks)

        # 4. Evaluate vector DB & retrieval
        await self.evaluate_vector_db_and_retrieval(chunks, test_queries)

        # 5. Evaluate RAG service (only if API key available)
        if settings.GROQ_API_KEY and settings.GROQ_API_KEY != "":
            await self.evaluate_rag_service(test_queries)
        else:
            self.results["rag_service"] = {
                "status": "skipped",
                "reason": "GROQ_API_KEY not set"
            }
            logger.info("Skipping RAG service evaluation: GROQ_API_KEY not set")

        # 6. Evaluate end-to-end
        await self.evaluate_end_to_end(sample_file, test_queries)

        # Save and print results
        self.save_results()
        self.print_summary()

        logger.info("Full evaluation complete!")


async def main():
    """Main entry point for evaluation"""
    evaluator = PolyDocEvaluator()
    await evaluator.run_full_evaluation()


if __name__ == "__main__":
    asyncio.run(main())
