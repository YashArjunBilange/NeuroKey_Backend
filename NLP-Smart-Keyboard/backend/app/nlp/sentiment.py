import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure lexicon is downloaded
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str):
    if not text.strip():
        return {"label": "Neutral", "score": 0.0, "details": {}}
        
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
        
    return {
        "label": label,
        "score": compound,
        "details": scores
    }
