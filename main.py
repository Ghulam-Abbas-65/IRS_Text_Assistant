

import json
from uptodate_24_hour_scrap import scrape_irs_data
from embeddings_manager import EmbeddingsManager
from knowledge_base import KnowledgeBase
from rag_assistant import RAGAssistant

def main():
    embeddings_manager = EmbeddingsManager()
    knowledge_base = KnowledgeBase(embeddings_manager)
    existing_data = scrape_irs_data()
    knowledge_base.update_documents(existing_data)
    
    rag_assistant = RAGAssistant(knowledge_base)
    
    while True:
        query = input("\nEnter your tax-related question: ")
        if query.lower() == 'quit':
            break
        
        response = rag_assistant.answer_query(query)
        print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
