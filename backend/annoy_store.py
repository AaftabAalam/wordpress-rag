import os
import numpy as np
from annoy import AnnoyIndex

class VectorStore:
    def __init__(self, embedding_dim=384, num_trees=400):
        self.embedding_dim = embedding_dim
        self.index = AnnoyIndex(self.embedding_dim, 'angular')
        self.num_trees = num_trees
        self.index_to_doc_id = {}
        self.current_index = 0

    def add_embedding(self, embedding, doc_id):
        if not hasattr(embedding, 'shape') or len(embedding.shape) == 0:
            raise ValueError("Invalid embedding shape.")
        if embedding.shape[0] != self.embedding_dim:
            raise ValueError(f"Embedding dimension mismatch: expected {self.embedding_dim}, got {embedding.shape[0]}")

        embedding = np.array(embedding).astype('float32')
        self.index.add_item(self.current_index, embedding)
        self.index_to_doc_id[self.current_index] = doc_id
        self.current_index += 1

    def build_index(self):
        self.index.build(self.num_trees)

    def search(self, query_embedding, top_k=1):
        query_embedding = np.array(query_embedding).astype('float32')
        indices, distances = self.index.get_nns_by_vector(query_embedding, top_k, include_distances=True)
        doc_ids = [self.index_to_doc_id[i] for i in indices]
        return distances, doc_ids

    def save_index(self, file_path="../annoy_indexes/annoy_index.ann"):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.index.save(file_path)

    def load_index(self, file_path="../annoy_indexes/annoy_index.ann"):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The index file at {file_path} does not exist.")
        self.index.load(file_path)