from collections import defaultdict, Counter
import math
from app.nlp.tokenizer import tokenize_text

class NGramModel:
    def __init__(self):
        self.unigrams = Counter()
        self.bigrams = Counter()
        self.trigrams = Counter()
        self.vocab_size = 0
        self.total_words = 0
        self.is_trained = False
        
    def train(self, corpus: list[str]):
        """Train the N-Gram model on a corpus of sentences"""
        self.unigrams.clear()
        self.bigrams.clear()
        self.trigrams.clear()
        
        for text in corpus:
            tokens = tokenize_text(text)["tokens"]
            # Convert to lowercase for better matching
            tokens = [t.lower() for t in tokens]
            
            # Unigrams
            self.unigrams.update(tokens)
            self.total_words += len(tokens)
            
            # Bigrams
            if len(tokens) >= 2:
                for i in range(len(tokens) - 1):
                    self.bigrams[(tokens[i], tokens[i+1])] += 1
                    
            # Trigrams
            if len(tokens) >= 3:
                for i in range(len(tokens) - 2):
                    self.trigrams[(tokens[i], tokens[i+1], tokens[i+2])] += 1
                    
        self.vocab_size = len(self.unigrams)
        self.is_trained = True
        
    def get_unigram_prob(self, word: str) -> float:
        """P(w) with Laplace smoothing"""
        count = self.unigrams.get(word.lower(), 0)
        return (count + 1) / (self.total_words + self.vocab_size)
        
    def get_bigram_prob(self, word1: str, word2: str) -> float:
        """P(w2|w1) with Laplace smoothing"""
        w1, w2 = word1.lower(), word2.lower()
        bg_count = self.bigrams.get((w1, w2), 0)
        w1_count = self.unigrams.get(w1, 0)
        return (bg_count + 1) / (w1_count + self.vocab_size)
        
    def get_trigram_prob(self, word1: str, word2: str, word3: str) -> float:
        """P(w3|w1,w2) with Laplace smoothing"""
        w1, w2, w3 = word1.lower(), word2.lower(), word3.lower()
        tg_count = self.trigrams.get((w1, w2, w3), 0)
        bg_count = self.bigrams.get((w1, w2), 0)
        
        # If bigram didn't exist, fall back to vocabulary size smoothing
        denominator = bg_count + self.vocab_size if bg_count > 0 else self.vocab_size
        return (tg_count + 1) / denominator

# Global instance
ngram_engine = NGramModel()

def calculate_sequence_probability(text: str):
    """Calculates log probability of a sequence using N-Gram model"""
    tokens = tokenize_text(text)["tokens"]
    if not tokens:
        return {"probability": 0.0, "log_prob": 0.0, "details": []}
        
    tokens = [t.lower() for t in tokens]
    
    # We need a trained model, if not trained, provide dummy output or train on a small sample
    if not ngram_engine.is_trained:
        # Dummy training for demonstration if no corpus was loaded
        sample_corpus = [
            "I am going home",
            "Are you coming to college tomorrow",
            "Yes I will be there around 9",
            "I have an exam tomorrow",
            "I am going to college"
        ]
        ngram_engine.train(sample_corpus)
        
    log_prob = 0.0
    details = []
    
    # Calculate trigram probability for the sequence
    for i in range(len(tokens)):
        if i == 0:
            prob = ngram_engine.get_unigram_prob(tokens[i])
            desc = f"P({tokens[i]})"
        elif i == 1:
            prob = ngram_engine.get_bigram_prob(tokens[i-1], tokens[i])
            desc = f"P({tokens[i]} | {tokens[i-1]})"
        else:
            prob = ngram_engine.get_trigram_prob(tokens[i-2], tokens[i-1], tokens[i])
            desc = f"P({tokens[i]} | {tokens[i-2]}, {tokens[i-1]})"
            
        # Avoid log(0)
        prob = max(prob, 1e-10)
        log_prob += math.log(prob)
        details.append({"step": desc, "probability": prob, "log_probability": math.log(prob)})
        
    return {
        "text": text,
        "log_probability": log_prob,
        "probability": math.exp(log_prob),
        "details": details
    }
