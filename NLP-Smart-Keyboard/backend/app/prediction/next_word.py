from app.nlp.ngrams import ngram_engine
from app.nlp.tokenizer import tokenize_text
import math

def predict_next_words(text: str, top_k: int = 3):
    """Predicts next words based on N-Gram model"""
    if not ngram_engine.is_trained:
        # Train on sample if not trained
        sample_corpus = [
            "I am going home",
            "I am going to college",
            "I am going there",
            "Are you coming to college tomorrow",
            "Yes I will be there around 9",
            "I have an exam tomorrow"
        ]
        ngram_engine.train(sample_corpus)
        
    tokens = tokenize_text(text)["tokens"]
    if not tokens:
        return {"predictions": []}
        
    tokens = [t.lower() for t in tokens]
    
    predictions = []
    
    # Try trigram first, then fallback to bigram, then unigram
    vocab = ngram_engine.unigrams.keys()
    
    if len(tokens) >= 2:
        w1, w2 = tokens[-2], tokens[-1]
        for v in vocab:
            if v not in [".", ",", "?", "!"]:
                prob = ngram_engine.get_trigram_prob(w1, w2, v)
                predictions.append({"word": v, "probability": prob, "model": "trigram"})
                
    elif len(tokens) == 1:
        w1 = tokens[-1]
        for v in vocab:
             if v not in [".", ",", "?", "!"]:
                prob = ngram_engine.get_bigram_prob(w1, v)
                predictions.append({"word": v, "probability": prob, "model": "bigram"})
                
    else:
        for v in vocab:
             if v not in [".", ",", "?", "!"]:
                prob = ngram_engine.get_unigram_prob(v)
                predictions.append({"word": v, "probability": prob, "model": "unigram"})
                
    # Sort and take top K
    predictions.sort(key=lambda x: x["probability"], reverse=True)
    
    # Deduplicate while preserving order
    seen = set()
    unique_preds = []
    for p in predictions:
        if p["word"] not in seen:
            seen.add(p["word"])
            unique_preds.append(p)
            if len(unique_preds) == top_k:
                break
                
    return {"predictions": unique_preds}
