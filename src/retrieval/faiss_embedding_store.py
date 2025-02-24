import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


def load_processed_data(json_file: str):
    """
    Loads the processed documents (and their chunks) from a JSON file.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def get_all_chunks(processed_docs):
    """
    Extracts all the chunks across documents along with simple metadata.
    
    Returns:
        texts: List[str] with all text chunks.
        metadata: List[dict] mapping the index to document_id, chunk index, and text.
    """
    texts = []
    metadata = []
    for doc in processed_docs:
        doc_id = doc['document_id']
        for i, chunk in enumerate(doc['chunks']):
            texts.append(chunk)
            metadata.append({
                'document_id': doc_id,
                'chunk_index': i,
                'chunk_text': chunk
            })
    return texts, metadata


def embed_texts(texts, model_name='all-MiniLM-L6-v2'):
    """
    Embeds input texts using a SentenceTransformer model.
    """
    model = SentenceTransformer(model_name)
    # Generate embeddings for all text chunks.
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings


def build_faiss_index(embeddings, embedding_dim):
    """
    Builds a FAISS index from the given embeddings using L2 distance.
    """
    # Create a flat L2 index
    index = faiss.IndexFlatL2(embedding_dim)
    # Ensure embeddings are in float32
    embeddings = np.array(embeddings).astype('float32')
    index.add(embeddings)
    return index


def main():
    # File paths and configurations
    processed_json = "data/clean/processed_data.json"  # already processed data (document chunks)
    index_path = "data/faiss_index.index"              # file to store the FAISS index
    metadata_path = "data/faiss_metadata.json"         # file to store metadata mapping
    
    # Load processed document chunks.
    processed_docs = load_processed_data(processed_json)
    texts, metadata = get_all_chunks(processed_docs)
    print(f"Total number of chunks: {len(texts)}")
    
    # Create embeddings for the chunks.
    embeddings = embed_texts(texts)
    embedding_dim = embeddings.shape[1]
    print(f"Embedding dimension: {embedding_dim}")
    
    # Build the FAISS index.
    index = build_faiss_index(embeddings, embedding_dim)
    
    # Save the FAISS index to disk.
    faiss.write_index(index, index_path)
    # Save metadata to help map FAISS index IDs back to document and chunk information.
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"FAISS index saved to: {index_path}")
    print(f"Metadata saved to: {metadata_path}")


if __name__ == "__main__":
    main()
