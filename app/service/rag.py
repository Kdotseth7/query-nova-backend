from core.config import settings
import faiss
import pandas as pd
from sqlalchemy.orm import Session

class Rag:
    def insert_embeddings(self, vectors):
        index = faiss.IndexFlatL2(vectors.shape[1])
        index.add(vectors)
        return index
    
    def similarity_search(self, query_vector, index, k=5):
        _, I = index.search(query_vector, k)
        return I
        
    def filter_tables(self, query: str, schema_info: dict) -> list:
        pass        