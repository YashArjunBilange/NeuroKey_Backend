from app.nlp.embeddings import get_embeddings, cosine_similarity

# Simple retrieval-based sentence prediction for demonstration
# In a real app, this would be a generative model or a large retrieval index
SENTENCE_DATABASE = [
    {"context": "I have an exam tomorrow", "responses": ["I should start preparing today.", "Maybe I'll study tonight.", "I hope I can do well."]},
    {"context": "Are you coming to college tomorrow", "responses": ["Yes, I'll be there around 9 AM.", "No, I am taking a day off.", "I haven't decided yet."]},
    {"context": "How are you", "responses": ["I am doing well, thank you.", "I'm good! How about you?", "Been better, but hanging in there."]},
    {"context": "I am planning a trip", "responses": ["That sounds exciting! Where to?", "Nice! When are you going?", "I love traveling."]}
]

def predict_next_sentence(context_text: str, top_k: int = 3):
    if not context_text.strip():
        return {"predictions": []}
        
    best_match = None
    highest_sim = -1.0
    
    # Find the most similar context in our database
    for item in SENTENCE_DATABASE:
        sim_data = cosine_similarity(
            get_embeddings([context_text])["embeddings"][0],
            get_embeddings([item["context"]])["embeddings"][0]
        )
        if sim_data > highest_sim:
            highest_sim = sim_data
            best_match = item
            
    # If we found a reasonable match
    if best_match and highest_sim > 0.4:
        predictions = [{"sentence": r, "confidence": highest_sim} for r in best_match["responses"]]
        return {"predictions": predictions[:top_k]}
        
    return {"predictions": []}
