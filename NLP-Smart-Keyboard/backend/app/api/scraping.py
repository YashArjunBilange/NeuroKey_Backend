from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
import httpx
from bs4 import BeautifulSoup
from app.nlp.language import detect_language
from app.nlp.sentiment import analyze_sentiment
from app.nlp.tokenizer import tokenize_text

router = APIRouter()

class ScrapeRequest(BaseModel):
    url: HttpUrl

@router.post("/scrape")
async def scrape_url(request: ScrapeRequest):
    url_str = str(request.url)
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url_str)
            response.raise_for_status()
            html = response.text
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail=f"Connection failure: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e.response.status_code}")
        
    soup = BeautifulSoup(html, "html.parser")
    
    title = soup.title.string if soup.title else "No title found"
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()
        
    text = soup.get_text(separator=' ')
    
    # Clean text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    cleaned_text = ' '.join(chunk for chunk in chunks if chunk)
    
    if not cleaned_text:
        raise HTTPException(status_code=400, detail="No extractable text found on page")
        
    # We truncate text for NLP analysis to avoid huge payloads/processing
    text_to_analyze = cleaned_text[:5000]
    
    lang_info = detect_language(text_to_analyze)
    token_info = tokenize_text(text_to_analyze)
    sentiment_info = analyze_sentiment(text_to_analyze)
    
    return {
        "title": title,
        "extracted_text": text_to_analyze,
        "word_count": token_info["word_count"],
        "sentence_count": token_info["sentence_count"],
        "language": lang_info["language"],
        "sentiment": sentiment_info["label"],
        "url": url_str
    }
