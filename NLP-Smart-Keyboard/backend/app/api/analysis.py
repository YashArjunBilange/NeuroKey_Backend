from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()

# Path to dataset
DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "data")
HUFFPOST_FILE = os.path.join(DATASET_DIR, "huffpost", "News_Category_Dataset_v3.json")
SAMPLE_FILE = os.path.join(DATASET_DIR, "sample", "sample_dataset.json")

# Sample data creation if it doesn't exist
def ensure_sample_data():
    os.makedirs(os.path.dirname(SAMPLE_FILE), exist_ok=True)
    if not os.path.exists(SAMPLE_FILE):
        data = [
            {"category": "TECH", "headline": "New AI Model Released", "short_description": "A new language model shows promising results."},
            {"category": "SPORTS", "headline": "Local Team Wins Championship", "short_description": "The city celebrates as the team secures a massive victory."},
            {"category": "POLITICS", "headline": "Election Results Announced", "short_description": "Voter turnout reached a record high this year."},
            {"category": "ENTERTAINMENT", "headline": "Blockbuster Movie Breaks Records", "short_description": "Audiences flock to cinemas for the highly anticipated sequel."}
        ]
        df = pd.DataFrame(data)
        df.to_json(SAMPLE_FILE, orient="records", lines=True)

ensure_sample_data()

@router.get("/dataset/analysis")
async def analyze_dataset(use_sample: bool = True):
    file_path = SAMPLE_FILE if use_sample else HUFFPOST_FILE
    
    if not os.path.exists(file_path):
        return {
            "error": "Dataset not found",
            "message": f"Please add the dataset to {file_path}"
        }
        
    try:
        df = pd.read_json(file_path, lines=True)
        
        category_counts = df['category'].value_counts().to_dict()
        total_articles = len(df)
        
        # Calculate some basic statistics
        df['word_count'] = df['headline'].apply(lambda x: len(str(x).split()))
        avg_word_count = float(df['word_count'].mean())
        
        return {
            "status": "success",
            "total_articles": total_articles,
            "categories": list(category_counts.keys()),
            "category_distribution": category_counts,
            "average_headline_word_count": round(avg_word_count, 2)
        }
    except Exception as e:
        return {"error": str(e)}
