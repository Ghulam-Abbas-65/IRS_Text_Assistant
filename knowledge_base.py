
from typing import Dict, List, Tuple
import numpy as np
from datetime import datetime
import json

class KnowledgeBase:
    def __init__(self, embeddings_manager):
        self.embeddings_manager = embeddings_manager
        self.documents: Dict[str, str] = {}
        self.last_updated = None

    def update_documents(self, new_documents: Dict[str, str]):
   
        self.documents.update(new_documents)
        self.embeddings_manager.get_embeddings(new_documents)  # Fix method call
        self.last_updated = datetime.now()

    def find_relevant_documents(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        
        query_embedding = self.embeddings_manager.create_embedding(query)
        
        similarities = []
        for url, doc_embedding in self.embeddings_manager.embeddings_cache.items():
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarities.append((url, similarity))
        
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
