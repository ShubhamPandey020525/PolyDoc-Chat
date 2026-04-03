from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from src_ai.core.config import settings
from src_ai.core.logger import logger
from src_ai.retrievers.hybrid_retriever import HybridRetriever
from src_ai.models.reranker import Reranker
from typing import List, Dict, Any

class CitationFormatter:
    """Utility to format sources and citations for Grok's output."""
    @staticmethod
    def format_citation(metadata: Dict[str, Any]) -> str:
        source = metadata.get("source", "Unknown")
        page = metadata.get("page_number")
        row = metadata.get("row_index")
        citation = f"[{source}]"
        if page: citation += f" (Page: {page})"
        if row: citation += f" (Row: {row})"
        return citation

    @classmethod
    def format_all_citations(cls, metadata_list: List[Dict[str, Any]]) -> str:
        unique = {cls.format_citation(m) for m in metadata_list}
        return "\n".join(list(unique))

class GrokQueryEngine:
    """Professional RAG Service using xAI (Grok) API."""
    def __init__(self, retriever: HybridRetriever):
        self.retriever = retriever
        self.reranker = Reranker()
        self.llm = ChatOpenAI(
            model=settings.GROK_MODEL,
            openai_api_key=settings.XAI_API_KEY,
            openai_api_base=settings.XAI_BASE_URL,
            temperature=0.1
        )

    def process(self, query: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        logger.info("Starting professional RAG pipeline with Grok", query=query)
        
        # 1. Hybrid Retrieval
        candidates = self.retriever.search(query, top_k=settings.RETRIEVAL_TOP_K)
        
        # 2. Professional Reranking
        refined_docs = self.reranker.rerank(query, candidates, top_k=settings.RERANK_TOP_K)
        
        # 3. Context & Citation Prep
        context_text = "\n\n".join([f"Source {i+1}:\n{doc['content']}" for i, doc in enumerate(refined_docs)])
        citations = CitationFormatter.format_all_citations([doc["metadata"] for doc in refined_docs])
        
        # 4. Prompt Engineering
        system_prompt = f"""You are a senior AI analyst. Answer based ONLY on the provided context.
Use a professional, clear, and structured tone.
Cite your sources explicitly.

CONTEXT:
{context_text}
"""
        messages = [SystemMessage(content=system_prompt)]
        if conversation_history:
            for turn in conversation_history:
                role = turn.get("role", "user")
                content = turn.get("content", "")
                messages.append(HumanMessage(content=content) if role == "user" else SystemMessage(content=content))
        messages.append(HumanMessage(content=query))
        
        # 5. LLM Call
        try:
            response = self.llm.invoke(messages)
            return {
                "answer": response.content,
                "citations": citations,
                "sources": refined_docs
            }
        except Exception as e:
            logger.error("Grok API call failed", error=str(e))
            return {
                "answer": "I apologize, but I encountered an error while processing your request with the Grok API.",
                "citations": "",
                "sources": []
            }
