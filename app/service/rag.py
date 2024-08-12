import os
import faiss
import numpy as np
from llm.openai_llm import OpenAILLM
import logging

class Rag:
    def __init__(self, index_path: str = "faiss_index.index"):
        self.index_path = index_path
        self.index = None
    
    def insert_embeddings(self, vectors) -> faiss.IndexHNSWFlat:
        DIMENSION = vectors.shape[1]
        NEIGHBORS = 32
        index = faiss.IndexHNSWFlat(DIMENSION, NEIGHBORS)
        index.hnsw.efConstruction = 40
        index.add(vectors)
        return index
    
    def save_index(self, index: faiss.IndexHNSWFlat):
        faiss.write_index(index, self.index_path)
    
    def load_index(self) -> faiss.IndexHNSWFlat:
        return faiss.read_index(self.index_path)
    
    def similarity_search(self, query_vector, index, k=5) -> list:
        _, I = index.search(query_vector, k)
        return I
    
    def extract_table_names(self, table_descriptions: list) -> list:
        table_names = []
        for description in table_descriptions:
            name_line = next((line for line in description.split('\n') if "Table Name:" in line), None)
            if name_line:
                table_name = name_line.split("Table Name:")[1].strip()
                table_names.append(table_name)
        return table_names
    
    def filter_tables(self, query: str, table_descriptions: list) -> tuple[list, list]:
        openai_llm = OpenAILLM()
        
        if os.path.exists(self.index_path):
            print("Loading existing FAISS index...")
            index = self.load_index()
        else:
            print("Creating a new FAISS index...")
            embedding_vectors = openai_llm.get_embeddings(table_descriptions)
            index = self.insert_embeddings(embedding_vectors)
            self.save_index(index)
        
        query_vector = openai_llm.get_embeddings([query])
        table_indices = self.similarity_search(query_vector, index)
        
        # Extract table names using indices
        table_names = self.extract_table_names(table_descriptions)
        selected_table_names = [table_names[i] for i in table_indices[0]]
        selected_table_names_info = [table_descriptions[i] for i in table_indices[0]]
        
        return selected_table_names, selected_table_names_info
