

import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os
import json
from datetime import datetime
import logging

class EmbeddingsManager:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.embeddings_file = 'embeddings_cache.pkl'
        self.metadata_file = 'embeddings_metadata.json'
        self.embeddings_cache = {}
        self.load_cached_embeddings()

    def load_cached_embeddings(self):
        """Loads embeddings from cache."""
        try:
            if os.path.exists(self.embeddings_file):
                with open(self.embeddings_file, 'rb') as f:
                    self.embeddings_cache = pickle.load(f)
                logging.info("✅ Loaded cached embeddings")
            else:
                logging.info("⚠️ No cached embeddings found")
        except Exception as e:
            logging.error(f"Error loading embeddings: {e}")

    def save_embeddings(self):
        """Saves embeddings to cache."""
        try:
            print(f"🔍 DEBUG: Saving {len(self.embeddings_cache)} embeddings...")  
            with open(self.embeddings_file, 'wb') as f:
                pickle.dump(self.embeddings_cache, f)
            
            metadata = {
                'last_updated': datetime.now().isoformat(),
                'num_documents': len(self.embeddings_cache)
            }
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)
            logging.info("✅ Saved embeddings to cache")
        except Exception as e:
            logging.error(f"Error saving embeddings: {e}")

    def create_embedding(self, text: str) -> np.ndarray:
        """Creates an embedding vector for a given text."""
        return self.model.encode(text)

    def get_embeddings(self, text_dict: dict) -> dict:
        """Gets embeddings for new documents and updates cache."""
        new_embeddings = {}
        updated = False

        for url, text in text_dict.items():
            if url not in self.embeddings_cache:
                try:
                    embedding = self.create_embedding(text)
                    self.embeddings_cache[url] = embedding
                    new_embeddings[url] = embedding
                    updated = True
                except Exception as e:
                    logging.error(f"Error creating embedding for {url}: {e}")
                    continue
            else:
                new_embeddings[url] = self.embeddings_cache[url]

        if updated:
            self.save_embeddings()

        return new_embeddings
