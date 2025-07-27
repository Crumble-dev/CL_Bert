from transformers import pipeline
import torch

# Modelo multilingüe (español incluido)
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment(text: str):
    result = sentiment_pipeline(text)[0]
    label = result['label']  # e.g., '4 stars'
    score = float(result['score'])

    if "1" in label or "2" in label:
        sentiment = "negative"
    elif "3" in label:
        sentiment = "neutral"
    else:
        sentiment = "positive"

    return sentiment, score
