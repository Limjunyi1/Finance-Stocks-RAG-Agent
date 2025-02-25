import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


def load_faiss_index(index_path: str):
    """
    Loads the FAISS index from disk.
    """
    return faiss.read_index(index_path)


def load_metadata(metadata_path: str):
    """
    Loads the metadata JSON that maps FAISS index positions to document chunks.
    """
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return metadata


def embed_query(query: str, model_name='all-MiniLM-L6-v2'):
    """
    Embeds the query using a SentenceTransformer model.
    Returns a numpy array of shape (1, embedding_dim) in float32.
    """
    model = SentenceTransformer(model_name)
    query_embedding = model.encode([query], show_progress_bar=False)
    query_embedding = np.array(query_embedding).astype('float32')
    return query_embedding


def retrieve_documents(query: str,
                       index_path: str = "data/faiss_index.index",
                       metadata_path: str = "data/faiss_metadata.json",
                       model_name: str = "all-MiniLM-L6-v2",
                       top_k: int = 3):
    """
    Retrieves the top-k most similar document chunks from the vector database given a query.
    
    Returns:
        List[dict]: List of metadata dictionaries for the top similar chunks.
    """
    index = load_faiss_index(index_path)
    metadata = load_metadata(metadata_path)
    query_embedding = embed_query(query, model_name=model_name)
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for idx in indices[0]:
        # Make sure we are within the bounds of our metadata list.
        if idx < len(metadata):
            results.append(metadata[idx])
    return results
