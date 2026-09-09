import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from app.nlp.tokenizer import tokenize_text
from app.nlp.pos_tagging import get_wordnet_pos, tag_pos

# Ensure resources are downloaded
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

def lemmatize_text(text: str):
    if not text.strip():
        return {"mapping": []}
        
    pos_data = tag_pos(text)
    tagged_tokens = pos_data.get("tagged_tokens", [])
    
    mapping = []
    for word, tag in tagged_tokens:
        wn_pos = get_wordnet_pos(tag)
        if wn_pos:
            lemma = lemmatizer.lemmatize(word, pos=wn_pos)
        else:
            lemma = lemmatizer.lemmatize(word)
            
        mapping.append({
            "word": word,
            "pos": tag,
            "lemma": lemma
        })
        
    return {"mapping": mapping}
