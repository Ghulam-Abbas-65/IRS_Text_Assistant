
import os
import json
import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class RAGAssistant:
    def __init__(self, knowledge_base):
        """Initialize RAG Assistant."""
        self.knowledge_base = knowledge_base
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.gemini_api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in environment variables. Please check your .env file.")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            api_key=self.gemini_api_key,
        )

    def answer_query(self, query: str) -> Dict[str, Any]:
       
        relevant_docs = self.knowledge_base.find_relevant_documents(query)
        context = "\n".join([f"Source ({url}): {self.knowledge_base.documents.get(url, '')}" for url, _ in relevant_docs])

        if not context:
            return {"answer": "No relevant documents found.", "sources": [], "timestamp": datetime.now().isoformat()}

        prompt = f"Query: {query}\nRelevant Documentation:\n{context}\nProvide a factual response with source citations."
        
        response = self.llm.invoke(prompt)
        answer = response.content.strip() if hasattr(response, "content") else "No response generated."
        
        return {
            "answer": answer,
            "sources": [url for url, _ in relevant_docs],
            "timestamp": datetime.now().isoformat()
        }
