from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from sqlalchemy.sql import func
from src.db.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, index=True)
    source = Column(String, index=True, nullable=False) # e.g. "amazon", "yelp"
    timestamp = Column(DateTime(timezone=True), default=func.now(), index=True)
    rating = Column(Float, nullable=True)
    original_text = Column(Text, nullable=False)
    cleaned_text = Column(Text, nullable=True)
    
    # NLP / Model Predictions
    sentiment_score = Column(Float, nullable=True)
    sentiment_label = Column(String, nullable=True) # e.g. "positive", "negative", "neutral"
    topic_id = Column(Integer, nullable=True)
    topic_label = Column(String, nullable=True)
    
    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
