from core.config import settings
import faiss

class Rag:
    def insert_embeddings(self, vectors):
        index = faiss.IndexFlatL2(vectors.shape[1])
        index.add(vectors)
        return index
    
    def similarity_search(self, query_vector, index, k=5):
        _, I = index.search(query_vector, k)
        return I

    def create_embeddings(self, schema: str) -> str:
        combined_desriptions = []
        