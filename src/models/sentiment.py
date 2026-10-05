from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, Any

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyzes the sentiment of a given text using VADER.
        
        Args:
            text: The cleaned review text.
            
        Returns:
            A dictionary containing the compound score and a label 
            ('positive', 'negative', 'neutral').
        """
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

    def analyze_batch(self, texts: list[str]) -> list[Dict[str, Any]]:
        """
        Analyzes a batch of texts.
        """
        return [self.analyze_text(t) for t in texts]

# Singleton instance for the API
sentiment_analyzer = SentimentAnalyzer()
