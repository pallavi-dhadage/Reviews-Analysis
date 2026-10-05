from typing import Dict, Any
from src.config import settings

class BaseSentimentAnalyzer:
    def analyze_text(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError

class VaderSentimentAnalyzer(BaseSentimentAnalyzer):
    def __init__(self):
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        if not text or not isinstance(text, str):
            return {"score": 0.0, "label": "neutral"}
            
        scores = self.analyzer.polarity_scores(text)
        compound = scores["compound"]
        
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"
            
        return {
            "score": compound,
            "label": label
        }

class TransformerSentimentAnalyzer(BaseSentimentAnalyzer):
    def __init__(self):
        from transformers import pipeline
        # Use a lightweight robust model for production sentiment
        self.analyzer = pipeline(
            "sentiment-analysis", 
            model="distilbert-base-uncased-finetuned-sst-2-english",
            truncation=True, 
            max_length=512
        )
        
    def analyze_text(self, text: str) -> Dict[str, Any]:
        if not text or not isinstance(text, str):
            return {"score": 0.0, "label": "neutral"}
            
        # pipeline returns [{'label': 'POSITIVE', 'score': 0.99}]
        result = self.analyzer(text)[0]
        label = result['label'].lower()
        score = result['score'] if label == "positive" else -result['score']
        
        return {
            "score": score,
            "label": label
        }

def get_sentiment_analyzer() -> BaseSentimentAnalyzer:
    if settings.USE_TRANSFORMERS:
        try:
            return TransformerSentimentAnalyzer()
        except ImportError:
            print("Transformers library not installed. Falling back to VADER.")
            return VaderSentimentAnalyzer()
    else:
        return VaderSentimentAnalyzer()

# Singleton instance for the API
sentiment_analyzer = get_sentiment_analyzer()
