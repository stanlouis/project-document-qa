# core/vector_store.py
import chromadb
import uuid
from typing import List
from core.embeddings import get_embedding

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_data"):
        # Initialize a persistent client that saves to disk
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create a collection (think of this as a table in SQL)
        self.collection = self.client.get_or_create_collection(name="document_collection")

    def add_texts(self, texts: List[str]):
        """Embeds and stores a list of text chunks persistently."""
        if not texts:
            return

        # ChromaDB requires unique IDs for every document chunk
        ids = [str(uuid.uuid4()) for _ in texts]
        
        # Generate embeddings using our existing OpenAI function
        embeddings = [get_embedding(text) for text in texts]

        # Save to the database
        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids
        )

    def similarity_search(self, query: str, top_k: int = 3) -> List[str]:
        """Queries the database for the most similar chunks."""
        if self.collection.count() == 0:
            return []

        query_embedding = get_embedding(query)
        
        # ChromaDB handles the heavy lifting of the search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Extract the flat list of text chunks from the results
        if results['documents'] and len(results['documents']) > 0:
            return results['documents'][0]
        return []

    def has_documents(self) -> bool:
        """Helper to check if the database is empty."""
        return self.collection.count() > 0

    def clear_database(self):
        """Deletes all data to start fresh."""
        self.client.delete_collection("document_collection")
        self.collection = self.client.get_or_create_collection(name="document_collection")