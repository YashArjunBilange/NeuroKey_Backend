from fastapi import APIRouter
from pydantic import BaseModel
from app.nlp.ngrams import calculate_sequence_probability
from app.prediction.next_word import predict_next_words
from app.prediction.next_sentence import predict_next_sentence

router = APIRouter()

class TextRequest(BaseModel):
    text: str

class PredictWordRequest(BaseModel):
    text: str
    top_k: int = 3

class PredictSentenceRequest(BaseModel):
    context: str
    top_k: int = 3

@router.post("/probability")
async def sequence_probability(req: TextRequest):
    return calculate_sequence_probability(req.text)

@router.post("/next-word")
async def next_word(req: PredictWordRequest):
    return predict_next_words(req.text, req.top_k)

@router.post("/next-sentence")
async def next_sentence(req: PredictSentenceRequest):
    return predict_next_sentence(req.context, req.top_k)
