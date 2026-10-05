import pandas as pd
import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from src.db.models import Review
from src.preprocessing.text_cleaner import clean_text

def ingest_csv(
    file_path: str, 
    db: Session, 
    source_name: str, 
    text_col: str, 
    rating_col: Optional[str] = None,
    timestamp_col: Optional[str] = None
) -> int:
    """
    Ingests reviews from a CSV file into the database.
    
    Args:
        file_path: Path to the CSV file.
        db: SQLAlchemy DB Session.
        source_name: Name of the data source (e.g., 'amazon', 'yelp').
        text_col: Column name in CSV containing the review text.
        rating_col: Column name in CSV containing the rating (optional).
        timestamp_col: Column name in CSV containing the timestamp (optional).
        
    Returns:
        Number of records inserted.
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV {file_path}: {str(e)}")

    if text_col not in df.columns:
        raise ValueError(f"Text column '{text_col}' not found in CSV.")

    records = []
    for _, row in df.iterrows():
        original_text = str(row[text_col]) if pd.notnull(row[text_col]) else ""
        if not original_text.strip():
            continue
            
        cleaned_text = clean_text(original_text)
        
        rating = None
        if rating_col and rating_col in df.columns and pd.notnull(row[rating_col]):
            try:
                rating = float(row[rating_col])
            except ValueError:
                pass
                
        timestamp = datetime.utcnow()
        if timestamp_col and timestamp_col in df.columns and pd.notnull(row[timestamp_col]):
            try:
                timestamp = pd.to_datetime(row[timestamp_col]).to_pydatetime()
            except Exception:
                pass

        review = Review(
            id=str(uuid.uuid4()),
            source=source_name,
            timestamp=timestamp,
            rating=rating,
            original_text=original_text,
            cleaned_text=cleaned_text
        )
        records.append(review)

    if records:
        db.add_all(records)
        db.commit()
    
    return len(records)
