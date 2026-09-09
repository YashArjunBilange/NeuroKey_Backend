# Load spaCy model lazily to avoid startup overhead if not needed immediately
nlp_model = None

def get_spacy_model():
    global nlp_model
    if nlp_model is None:
        import spacy

        try:
            nlp_model = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if not downloaded properly
            nlp_model = spacy.blank("en")
    return nlp_model

def extract_entities(text: str):
    if not text.strip():
        return {"entities": []}
        
    nlp = get_spacy_model()
    doc = nlp(text)
    
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char
        })
        
    return {"entities": entities}
