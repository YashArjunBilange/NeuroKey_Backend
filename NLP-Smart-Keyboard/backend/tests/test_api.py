import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.nlp.language import detect_language
from app.nlp.sentiment import analyze_sentiment
from app.nlp.emotion import detect_emotion
from app.nlp.ngrams import ngram_engine

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}

def test_language_detection():
    # Test English
    res_en = detect_language("How are you today?")
    assert res_en["language"] == "en"
    
def test_sentiment_analysis():
    # Test Positive
    res_pos = analyze_sentiment("I absolutely love this new keyboard, it is fantastic!")
    assert res_pos["label"] == "Positive"
    
    # Test Negative
    res_neg = analyze_sentiment("This is a terrible experience, I hate it.")
    assert res_neg["label"] == "Negative"

def test_emotion_detection():
    # Test Happy
    res_happy = detect_emotion("I am so happy and excited for tomorrow!")
    assert res_happy["emotion"] in ["Happy", "Excited"]
    
    # Test Angry
    res_angry = detect_emotion("I am furious and very angry right now.")
    assert res_angry["emotion"] == "Angry"

def test_next_word_api():
    # Test the API endpoint for predictions
    response = client.post(
        "/api/v1/predict/next-word",
        json={"text": "I am going", "top_k": 3}
    )
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert isinstance(data["predictions"], list)
    assert len(data["predictions"]) == 3
    assert {item["word"] for item in data["predictions"]} >= {"home", "to", "there"}

def test_next_sentence_api():
    response = client.post(
        "/api/v1/predict/next-sentence",
        json={"context": "Are you coming to college tomorrow?", "top_k": 3}
    )
    assert response.status_code == 200
    predictions = response.json()["predictions"]
    assert len(predictions) == 3
    assert all(prediction["sentence"] for prediction in predictions)

def test_incomplete_word_completion_api():
    response = client.post(
        "/api/v1/predict/next-word",
        json={"text": "I am go", "top_k": 3}
    )
    assert response.status_code == 200
    predictions = response.json()["predictions"]
    assert predictions
    assert predictions[0]["word"] == "going"
    assert predictions[0]["model"] == "completion"
