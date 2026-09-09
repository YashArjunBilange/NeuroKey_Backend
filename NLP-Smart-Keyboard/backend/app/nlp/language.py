import re

from langdetect import detect_langs
import langdetect.detector_factory

# Set seed for reproducible results
langdetect.detector_factory.init_factory()

def detect_language(text: str):
    normalized = text.strip()
    if not normalized:
        return {"language": "unknown", "confidence": 0.0}

    devanagari_chars = len(re.findall(r"[\u0900-\u097F]", normalized))
    if devanagari_chars:
        return {"language": "hi", "confidence": 1.0}

    hinglish_markers = {
        "aaj", "kal", "hai", "ho", "hoga", "jaana", "jana", "karna",
        "kya", "kaise", "kab", "college", "yaar", "mujhe", "tum",
    }
    latin_words = set(re.findall(r"[a-z]+", normalized.lower()))
    if len(latin_words & hinglish_markers) >= 2:
        return {"language": "hinglish", "confidence": 0.8}

    try:
        # Get language probabilities
        langs = detect_langs(normalized)
        if langs:
            top_lang = langs[0]
            lang_code = top_lang.lang
            confidence = top_lang.prob

            if lang_code not in {"en", "hi"} and normalized.isascii():
                lang_code = "en"
                confidence = min(confidence, 0.5)
            return {
                "language": lang_code,
                "confidence": confidence
            }
        return {"language": "unknown", "confidence": 0.0}
    except Exception:
        return {"language": "unknown", "confidence": 0.0}
