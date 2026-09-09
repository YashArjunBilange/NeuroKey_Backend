from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def calculate_tfidf(documents: list[str]):
    if not documents or all(not doc.strip() for doc in documents):
        return {"vocabulary": [], "matrix": [], "top_keywords": []}
        
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
    except ValueError:
        # Happens if all documents contain only stop words
        return {"vocabulary": [], "matrix": [], "top_keywords": []}
        
    feature_names = vectorizer.get_feature_names_out()
    
    # Calculate average TF-IDF score for each word across all documents
    avg_scores = tfidf_matrix.mean(axis=0).A1
    
    # Get top keywords
    word_scores = list(zip(feature_names, avg_scores))
    word_scores.sort(key=lambda x: x[1], reverse=True)
    
    top_keywords = [{"word": word, "score": float(score)} for word, score in word_scores[:10]]
    
    # Format matrix for JSON response
    # We'll just return a simplified version
    dense_matrix = tfidf_matrix.todense().tolist()
    
    return {
        "vocabulary": feature_names.tolist(),
        "matrix": dense_matrix,
        "top_keywords": top_keywords
    }
