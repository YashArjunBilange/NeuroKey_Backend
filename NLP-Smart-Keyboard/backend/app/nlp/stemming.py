import nltk
from nltk.stem import PorterStemmer
from app.nlp.tokenizer import tokenize_text

# Initialize stemmer
stemmer = PorterStemmer()

def stem_text(text: str):
    if not text.strip():
        return {"original": [], "stemmed": [], "mapping": []}
        
    token_data = tokenize_text(text)
    tokens = token_data.get("tokens", [])
    
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    
    mapping = [{"original": orig, "stem": stem} for orig, stem in zip(tokens, stemmed_tokens)]
    
    return {
        "original": tokens,
        "stemmed": stemmed_tokens,
        "mapping": mapping
    }
