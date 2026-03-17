# core/embeddings.py
import numpy as np
from core.config import client

def get_embedding(text: str, model: str = "nomic-embed-text") -> np.ndarray:
    """Generates a numerical vector for the provided text."""
    response = client.embeddings.create(
        model=model,
        input=text
    )
    return np.array(response.data[0].embedding)