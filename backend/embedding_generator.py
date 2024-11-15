from transformers import AutoTokenizer, AutoModel
import numpy as np

class EmbeddingGenerator:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def generate_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

        outputs = self.model(**inputs)

        embeddings = outputs.last_hidden_state.mean(dim=1)

        embedding = embeddings.detach().numpy().flatten()

        if not isinstance(embedding, np.ndarray):
            embedding = np.array(embedding)
        if embedding.shape == ():
            raise ValueError("Generated embedding has no shape. Check the embedding generation logic.")
        if embedding.shape[0] != 384:
            raise ValueError(f"Embedding has incorrect length: expected 384, got {embedding.shape[0]}")

        return embedding