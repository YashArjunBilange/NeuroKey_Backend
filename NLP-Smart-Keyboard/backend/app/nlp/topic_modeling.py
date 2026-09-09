from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def perform_topic_modeling(documents: list[str], num_topics: int = 2):
    if not documents or len(documents) < 2:
        return {"topics": []}
        
    # We need a reasonable number of topics
    actual_num_topics = min(num_topics, len(documents))
    
    vectorizer = CountVectorizer(stop_words='english')
    try:
        doc_term_matrix = vectorizer.fit_transform(documents)
    except ValueError:
        return {"topics": []}
        
    lda_model = LatentDirichletAllocation(n_components=actual_num_topics, random_state=42)
    lda_model.fit(doc_term_matrix)
    
    feature_names = vectorizer.get_feature_names_out()
    
    topics = []
    for topic_idx, topic in enumerate(lda_model.components_):
        top_features_ind = topic.argsort()[:-5 - 1:-1]
        top_features = [feature_names[i] for i in top_features_ind]
        topics.append({
            "id": topic_idx + 1,
            "keywords": top_features
        })
        
    return {"topics": topics}
