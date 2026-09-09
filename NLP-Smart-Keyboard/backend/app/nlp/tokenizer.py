import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Ensure resources are downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def tokenize_text(text: str):
    if not text.strip():
        return {"sentences": [], "tokens": [], "word_count": 0, "sentence_count": 0}

    sentences = sent_tokenize(text)
    tokens = word_tokenize(text)
    
    return {
        "original_text": text,
        "sentences": sentences,
        "tokens": tokens,
        "word_count": len(tokens),
        "sentence_count": len(sentences)
    }
