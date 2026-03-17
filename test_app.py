# test_app.py
import pytest
import numpy as np
from unittest.mock import patch
from core.chunker import chunk_text
from core.vector_store import VectorStore

# ==========================================
# 1. Test the Text Chunker
# ==========================================
def test_chunk_text():
    """Ensure the chunker correctly splits text based on tokens and overlap."""
    # Create a dummy text that is roughly 600 words/tokens
    dummy_text = "word " * 600 
    
    # Chunk with max 500 tokens and 100 overlap
    chunks = chunk_text(dummy_text, max_tokens=500, overlap=100)
    
    # We expect at least 2 chunks since 600 > 500
    assert len(chunks) >= 2, "Text should be split into multiple chunks."
    
    # Ensure no chunk exceeds the max_tokens limit (roughly)
    # Tiktoken might vary slightly based on exact characters, but it shouldn't be 600.
    assert len(chunks[0].split()) <= 500, "Chunk exceeded maximum token limit."

# ==========================================
# 2. Test the Vector Store (with Mocked API)
# ==========================================
@pytest.fixture
def temp_vector_store(tmp_path):
    """Fixture to create a temporary ChromaDB instance for testing."""
    # tmp_path is a built-in pytest fixture that provides a temporary directory
    return VectorStore(persist_directory=str(tmp_path))

@patch("core.vector_store.get_embedding")
def test_vector_store_add_and_search(mock_get_embedding, temp_vector_store):
    """Ensure documents are added to ChromaDB and similarity search works."""
    
    # 1. Setup the mock to return a fixed numpy array whenever get_embedding is called
    mock_embedding = np.random.rand(1536).tolist() # OpenAI small embeddings are 1536 dims
    mock_get_embedding.return_value = mock_embedding
    
    # 2. Add dummy data to the store
    dummy_chunks = ["This is the first test chunk.", "Here is the second test chunk."]
    temp_vector_store.add_texts(dummy_chunks)
    
    # 3. Verify the database registered the chunks
    assert temp_vector_store.has_documents() == True
    assert temp_vector_store.collection.count() == 2
    
    # 4. Test the similarity search
    results = temp_vector_store.similarity_search("first test chunk", top_k=1)
    
    # Since we mocked the embedding to be identical every time, ChromaDB will 
    # just return the first match it finds, but we can at least verify it returns a string.
    assert len(results) == 1
    assert isinstance(results[0], str)

def test_vector_store_clear(temp_vector_store):
    """Ensure the database can be wiped clean."""
    # Note: We aren't testing the API here, just ChromaDB's local logic
    temp_vector_store.collection.add(
        documents=["Test doc"],
        embeddings=[[0.1] * 1536],
        ids=["id1"]
    )
    
    assert temp_vector_store.collection.count() == 1
    temp_vector_store.clear_database()
    assert temp_vector_store.collection.count() == 0