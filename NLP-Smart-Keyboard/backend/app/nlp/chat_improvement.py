# Simulated rule-based chat improvement
# In a real production environment, this would use a generative LLM (like Gemini or OpenAI)

STYLE_RULES = {
    "Professional": {
        "send me the file": "Could you please send me the file when you have a moment?",
        "ok": "Understood. I will proceed accordingly.",
        "what?": "Could you please clarify that?",
        "i don't know": "I'm currently looking into this and will get back to you.",
        "yes": "Yes, I agree.",
        "no": "I disagree, unfortunately.",
    },
    "Friendly": {
        "send me the file": "Hey! Can you send over that file when you get a chance? Thanks!",
        "ok": "Sounds good! 👍",
        "yes": "Yes, absolutely!",
    }
}

def improve_message(text: str, style: str = "Professional"):
    text_lower = text.strip().lower()
    
    rules = STYLE_RULES.get(style, STYLE_RULES["Professional"])
    
    # Check exact match
    if text_lower in rules:
        return {"original": text, "improved": rules[text_lower], "style": style}
        
    # If no rule matches, we just add some polite wrappers (naive implementation for demo)
    improved = text
    if style == "Professional":
        improved = f"Regarding your message: {text}. Could we discuss this further?"
    elif style == "Friendly":
        improved = f"Hey! {text} 😊"
        
    return {"original": text, "improved": improved, "style": style}
