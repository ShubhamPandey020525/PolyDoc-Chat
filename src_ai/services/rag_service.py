from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from src_ai.core.config import settings
from src_ai.core.logger import logger
from src_ai.retrievers.simple_retriever import SimpleRetriever
from typing import List, Dict, Any

class CitationFormatter:
    """Utility to format sources and citations for output."""
    @staticmethod
    def format_citation(metadata: Dict[str, Any]) -> str:
        source = metadata.get("source", "Unknown")
        page = metadata.get("page_number")
        slide = metadata.get("slide_number")
        row = metadata.get("row_index")
        
        citation = f"[{source}]"
        if page: citation += f" (Page: {page})"
        if slide: citation += f" (Slide: {slide})"
        if row: citation += f" (Row: {row})"
        return citation

    @classmethod
    def format_all_citations(cls, metadata_list: List[Dict[str, Any]]) -> str:
        unique = {cls.format_citation(m) for m in metadata_list}
        return "\n".join(list(unique))

class GrokQueryEngine:
    """Simple RAG Service using xAI (Grok) API with Async support."""
    def __init__(self, retriever: SimpleRetriever):
        self.retriever = retriever
        self.llm = ChatOpenAI(
            model=settings.GROK_MODEL,
            openai_api_key=settings.XAI_API_KEY,
            openai_api_base=settings.XAI_BASE_URL,
            temperature=0.1
        )

    async def process(self, query: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        logger.info("Starting simple RAG pipeline (Async)", query=query)
        
        # 1. Similarity Search
        docs = await self.retriever.search(query, top_k=settings.RETRIEVAL_TOP_K)
        
        if not docs:
            return {
                "answer": "I'm sorry, but I couldn't find any relevant information in the uploaded documents to answer your question.",
                "citations": "",
                "sources": []
            }

        # 2. Context & Citation Prep
        context_text = "\n\n".join([f"--- Source {i+1} ---\n{doc['content']}" for i, doc in enumerate(docs)])
        citations = CitationFormatter.format_all_citations([doc["metadata"] for doc in docs])
        
        # 3. Prompt Engineering
        system_prompt = f"""You are a professional AI assistant. Your task is to answer the user's question based ONLY on the provided context below.

Rules:
1. Use a professional, clear, and structured tone.
2. If the answer cannot be found in the provided context, clearly state: "I'm sorry, but this information is not available in the provided documents."
3. Do NOT use any external knowledge.
4. Cite your sources explicitly using the source numbers or names provided in the context.

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
        
        # 4. LLM Call
        try:
            response = await self.llm.ainvoke(messages)
            
            # Simple validation to ensure it doesn't hallucinate if it says it doesn't know
            answer = response.content
            if "not available in the provided documents" in answer.lower() or "couldn't find any relevant information" in answer.lower():
                citations = "" # No citations if info not found

            return {
                "answer": answer,
                "citations": citations,
                "sources": docs
            }
        except Exception as e:
            logger.error("LLM API call failed", error=str(e))
            return {
                "answer": "I apologize, but I encountered an error while processing your request.",
                "citations": "",
                "sources": []
            }
