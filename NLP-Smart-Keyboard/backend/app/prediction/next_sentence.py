import re

SENTENCE_DATABASE = [
    {"context": "I have an exam tomorrow", "responses": ["I should start preparing today.", "Maybe I'll study tonight.", "I hope I can do well."]},
    {"context": "Are you coming to college tomorrow", "responses": ["Yes, I'll be there around 9 AM.", "No, I am taking a day off.", "I haven't decided yet."]},
    {"context": "How are you", "responses": ["I am doing well, thank you.", "I'm good! How about you?", "Been better, but hanging in there."]},
    {"context": "I am planning a trip", "responses": ["That sounds exciting! Where to?", "Nice! When are you going?", "I love traveling."]}
]

def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9']+", text.lower()))

def _overlap(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)

def predict_next_sentence(context_text: str, top_k: int = 3):
    if not context_text.strip():
        return {"predictions": []}
        
    context_tokens = _tokens(context_text)
    ranked = sorted(
        SENTENCE_DATABASE,
        key=lambda item: _overlap(context_tokens, _tokens(item["context"])),
        reverse=True,
    )
    best_match = ranked[0]
    confidence = _overlap(context_tokens, _tokens(best_match["context"]))

    if confidence == 0:
        fallback = [
            "I understand. Tell me more.",
            "That sounds good, let me know what happens.",
            "Thanks for sharing that with me.",
        ]
        return {"predictions": [{"sentence": text, "confidence": 0.2} for text in fallback[:top_k]]}

    return {
        "predictions": [
            {"sentence": response, "confidence": round(max(confidence, 0.35), 3)}
            for response in best_match["responses"][:top_k]
        ]
    }
