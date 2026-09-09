from app.nlp.sentiment import analyze_sentiment
import re

# Simple heuristic-based emotion detection for demonstration
# In production, this would be a classification model (e.g., fine-tuned BERT or zero-shot classifier)
EMOTION_KEYWORDS = {
    "Happy": ["happy", "glad", "joy", "great", "excellent", "awesome", "fantastic", "yay", "haha"],
    "Sad": ["sad", "depressed", "unhappy", "cry", "sorry", "terrible", "awful"],
    "Angry": ["angry", "mad", "furious", "hate", "annoying", "stupid"],
    "Excited": ["excited", "thrilled", "omg", "wow", "amazing", "can't wait"],
    "Love": ["love", "adore", "heart", "beautiful", "sweet"],
    "Fear": ["scared", "afraid", "terrified", "panic", "worry", "worried"],
    "Surprise": ["surprise", "shocked", "unexpected", "sudden"]
}

def detect_emotion(text: str):
    if not text.strip():
        return {"emotion": "Neutral", "confidence": 0.0}
        
    text_lower = text.lower()
    
    # Calculate scores based on keywords
    emotion_scores = {emo: 0 for emo in EMOTION_KEYWORDS}
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for kw in keywords:
            if re.search(r'\b' + kw + r'\b', text_lower):
                emotion_scores[emotion] += 1
                
    # Also consider sentiment
    sentiment_res = analyze_sentiment(text)
    if sentiment_res["label"] == "Positive":
        emotion_scores["Happy"] += 0.5
    elif sentiment_res["label"] == "Negative":
        emotion_scores["Sad"] += 0.5
        
    # Get top emotion
    top_emotion = max(emotion_scores.items(), key=lambda x: x[1])
    
    if top_emotion[1] > 0:
        # Normalize pseudo-confidence
        total_score = sum(emotion_scores.values())
        confidence = min(top_emotion[1] / total_score + 0.3, 0.95)
        return {"emotion": top_emotion[0], "confidence": round(confidence, 2)}
        
    return {"emotion": "Neutral", "confidence": 0.5}
