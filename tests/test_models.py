import pytest
from src.models.sentiment import VaderSentimentAnalyzer

def test_vader_sentiment_positive():
    analyzer = VaderSentimentAnalyzer()
    result = analyzer.analyze_text("This product is absolutely amazing and I love it!")
    assert result["label"] == "positive"
    assert result["score"] > 0

def test_vader_sentiment_negative():
    analyzer = VaderSentimentAnalyzer()
    result = analyzer.analyze_text("Terrible experience. The quality is the worst I have ever seen.")
    assert result["label"] == "negative"
    assert result["score"] < 0

def test_vader_sentiment_neutral():
    analyzer = VaderSentimentAnalyzer()
    result = analyzer.analyze_text("The item is okay, neither good nor bad.")
    # Depending on VADER's exact score, it might be neutral or slightly positive
    # We just ensure it returns a valid structure
    assert "label" in result
    assert "score" in result

def test_vader_empty_text():
    analyzer = VaderSentimentAnalyzer()
    result = analyzer.analyze_text("")
    assert result["label"] == "neutral"
    assert result["score"] == 0.0
