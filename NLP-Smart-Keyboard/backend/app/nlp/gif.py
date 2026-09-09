from app.nlp.emotion import detect_emotion
import os

def recommend_gif_query(text: str):
    if not text.strip():
        return {"query": "hello", "url": None}
        
    emotion_data = detect_emotion(text)
    emotion = emotion_data["emotion"]
    
    query = f"{emotion.lower()} reaction"
    
    # In a real app, you would call Giphy/Tenor API here using GIF_API_KEY
    # from app.config import settings
    # api_key = settings.GIF_API_KEY
    
    return {
        "query": query,
        "url": None, # Indicates frontend should use search UI or fallback
        "message": "API key required for actual GIF fetching"
    }
