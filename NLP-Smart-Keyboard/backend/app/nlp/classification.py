from app.nlp.sentiment import analyze_sentiment

def classify_text(text: str):
    """
    Text classification pipeline.
    For this project, we are classifying based on sentiment polarity using VADER.
    A more advanced version would use a trained model on a specific dataset.
    """
    if not text.strip():
        return {"text": text, "prediction": "Neutral", "confidence": 0.0}
        
    sentiment_result = analyze_sentiment(text)
    
    # Map compound score to confidence (0 to 1)
    confidence = abs(sentiment_result["score"])
    
    # If it's neutral and score is very low, we still want a baseline confidence
    if sentiment_result["label"] == "Neutral" and confidence < 0.1:
        confidence = 1.0 - confidence # High confidence that it is neutral
        
    return {
        "text": text,
        "prediction": sentiment_result["label"],
        "confidence": confidence
    }
