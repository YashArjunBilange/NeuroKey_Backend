from fastapi import APIRouter
from pydantic import BaseModel
from app.nlp import language, tokenizer, stemming, lemmatization, pos_tagging, ner, embeddings, tfidf, classification, sentiment, topic_modeling, emotion, vibe, emoji, gif, chat_improvement

router = APIRouter()

class TextRequest(BaseModel):
    text: str

class TextsRequest(BaseModel):
    texts: list[str]

class CompareRequest(BaseModel):
    text1: str
    text2: str

class TopicRequest(BaseModel):
    texts: list[str]
    num_topics: int = 2

class ImproveRequest(BaseModel):
    text: str
    style: str = "Professional"

@router.post("/language")
async def detect_lang(req: TextRequest):
    return language.detect_language(req.text)

@router.post("/tokenize")
async def tokenize(req: TextRequest):
    return tokenizer.tokenize_text(req.text)

@router.post("/stem")
async def stem(req: TextRequest):
    return stemming.stem_text(req.text)

@router.post("/lemmatize")
async def lemmatize(req: TextRequest):
    return lemmatization.lemmatize_text(req.text)

@router.post("/pos")
async def pos(req: TextRequest):
    return pos_tagging.tag_pos(req.text)

@router.post("/ner")
async def named_entities(req: TextRequest):
    return ner.extract_entities(req.text)

@router.post("/embeddings")
async def get_embeddings(req: TextsRequest):
    return embeddings.get_embeddings(req.texts)

@router.post("/embeddings/compare")
async def compare_embeddings(req: CompareRequest):
    return embeddings.compare_sentences(req.text1, req.text2)

@router.post("/tfidf")
async def get_tfidf(req: TextsRequest):
    return tfidf.calculate_tfidf(req.texts)

@router.post("/classify")
async def classify(req: TextRequest):
    return classification.classify_text(req.text)

@router.post("/sentiment")
async def get_sentiment(req: TextRequest):
    return sentiment.analyze_sentiment(req.text)

@router.post("/topics")
async def get_topics(req: TopicRequest):
    return topic_modeling.perform_topic_modeling(req.texts, req.num_topics)

@router.post("/emotion")
async def get_emotion(req: TextRequest):
    return emotion.detect_emotion(req.text)

@router.post("/vibe")
async def get_vibe(req: TextRequest):
    return vibe.detect_vibe(req.text)

@router.post("/emoji")
async def get_emoji(req: TextRequest):
    return emoji.recommend_emojis(req.text)

@router.post("/gif")
async def get_gif(req: TextRequest):
    return gif.recommend_gif_query(req.text)

@router.post("/improve")
async def get_improved_chat(req: ImproveRequest):
    return chat_improvement.improve_message(req.text, req.style)

