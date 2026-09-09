from app.nlp.emotion import detect_emotion
from app.nlp.sentiment import analyze_sentiment

# Mapping from emotions/keywords to emojis
EMOJI_MAP = {
    "Happy": ["😊", "😄", "🎉"],
    "Sad": ["😢", "😞", "💔"],
    "Angry": ["😠", "😡", "🤬"],
    "Excited": ["🤩", "🚀", "✨"],
    "Love": ["❤️", "😍", "💕"],
    "Fear": ["😨", "😱", "😰"],
    "Surprise": ["😲", "🤯", "😮"],
    "Neutral": ["👍", "👌", "🤔"]
}

def recommend_emojis(text: str):
    if not text.strip():
        return {"emojis": ["👍", "😊", "👋"]}
        
    emotion_data = detect_emotion(text)
    emotion = emotion_data["emotion"]
    
    emojis = EMOJI_MAP.get(emotion, EMOJI_MAP["Neutral"])
    
    # If neutral but very positive
    if emotion == "Neutral":
        sentiment = analyze_sentiment(text)
        if sentiment["label"] == "Positive":
            emojis = EMOJI_MAP["Happy"]
        elif sentiment["label"] == "Negative":
            emojis = EMOJI_MAP["Sad"]
            
    return {"emojis": emojis}
