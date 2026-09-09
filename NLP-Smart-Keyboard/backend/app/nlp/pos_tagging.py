import nltk
from nltk.corpus import wordnet
from app.nlp.tokenizer import tokenize_text

# Ensure resources are downloaded
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

def tag_pos(text: str):
    if not text.strip():
        return {"tagged_tokens": []}
        
    token_data = tokenize_text(text)
    tokens = token_data.get("tokens", [])
    
    tagged = nltk.pos_tag(tokens)
    
    return {"tagged_tokens": tagged}

def get_wordnet_pos(treebank_tag: str):
    """Convert treebank POS tags to WordNet POS tags for lemmatizer"""
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None
