from app.nlp.ngrams import ngram_engine
from app.nlp.tokenizer import tokenize_text

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
    
    top_k = max(1, min(top_k, 5))
    predictions = []
    vocab = [word for word in ngram_engine.unigrams if word not in {".", ",", "?", "!"}]

    if not text[-1].isspace():
        partial = tokens[-1]
        completions = [word for word in vocab if word.startswith(partial) and word != partial]
        if completions:
            return {
                "predictions": [
                    {
                        "word": word,
                        "probability": ngram_engine.get_unigram_prob(word),
                        "model": "completion"
                    }
                    for word in sorted(completions, key=lambda item: (-ngram_engine.unigrams[item], item))[:top_k]
                ]
            }

    if len(tokens) >= 2:
        w1, w2 = tokens[-2], tokens[-1]
        trigram_candidates = [
            (word3, count) for (word1, word2, word3), count in ngram_engine.trigrams.items()
            if word1 == w1 and word2 == w2 and word3 in vocab
        ]
        for word, count in sorted(trigram_candidates, key=lambda item: (-item[1], item[0])):
            predictions.append({"word": word, "probability": ngram_engine.get_trigram_prob(w1, w2, word), "model": "trigram", "count": count})

    if len(predictions) < top_k and tokens:
        w1 = tokens[-1]
        bigram_candidates = [
            (word2, count) for (word_left, word2), count in ngram_engine.bigrams.items()
            if word_left == w1 and word2 in vocab and word2 not in {item["word"] for item in predictions}
        ]
        for word, count in sorted(bigram_candidates, key=lambda item: (-item[1], item[0])):
            predictions.append({"word": word, "probability": ngram_engine.get_bigram_prob(w1, word), "model": "bigram", "count": count})

    if len(predictions) < top_k:
        used = {item["word"] for item in predictions}
        for word in sorted(vocab, key=lambda item: (-ngram_engine.unigrams[item], item)):
            if word in used:
                continue
            predictions.append({"word": word, "probability": ngram_engine.get_unigram_prob(word), "model": "unigram", "count": ngram_engine.unigrams[word]})
            if len(predictions) >= top_k:
                break

    return {
        "predictions": [
            {key: value for key, value in prediction.items() if key != "count"}
            for prediction in predictions[:top_k]
        ]
    }
