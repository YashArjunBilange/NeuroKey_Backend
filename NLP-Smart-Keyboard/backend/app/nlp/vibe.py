from app.nlp.sentiment import analyze_sentiment
from app.nlp.emotion import detect_emotion

def detect_vibe(text: str):
    if not text.strip():
        return {"vibe": "Neutral"}
        
    sentiment = analyze_sentiment(text)
    emotion = detect_emotion(text)
    
    # Combine sentiment, emotion and structural heuristics
    has_exclamation = "!" in text
    has_question = "?" in text
    is_short = len(text.split()) < 4
    
    if emotion["emotion"] in ["Happy", "Excited", "Love"]:
        return {"vibe": "Energetic" if has_exclamation else "Positive"}
        
    if emotion["emotion"] in ["Sad", "Angry", "Fear"]:
        return {"vibe": "Tense"}
        
    if sentiment["label"] == "Positive":
        return {"vibe": "Friendly"}
        
    if sentiment["label"] == "Negative":
        return {"vibe": "Negative"}
        
    if has_question:
        return {"vibe": "Inquisitive"}
        
    if is_short:
        return {"vibe": "Casual"}
        
    return {"vibe": "Professional/Neutral"}
