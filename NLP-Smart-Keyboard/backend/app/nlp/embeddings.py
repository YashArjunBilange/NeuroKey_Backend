import numpy as np

# Load model lazily
embedding_model = None

def get_embedding_model():
    global embedding_model
    if embedding_model is None:
        from sentence_transformers import SentenceTransformer

        # Use a lightweight model as requested
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return embedding_model

def get_embeddings(sentences: list[str]):
    if not sentences:
        return {"embeddings": [], "dimension": 0}
        
    model = get_embedding_model()
    embeddings = model.encode(sentences)
    
    return {
        "embeddings": embeddings.tolist(),
        "dimension": embeddings.shape[1] if len(embeddings) > 0 else 0
    }

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0.0
        
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def compare_sentences(sent1: str, sent2: str):
    model = get_embedding_model()
    embeddings = model.encode([sent1, sent2])
    
    similarity = cosine_similarity(embeddings[0].tolist(), embeddings[1].tolist())
    
    return {
        "sentence1": sent1,
        "sentence2": sent2,
        "similarity": similarity
    }
