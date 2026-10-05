from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
import shutil
import os

from src.db.database import get_db
from src.db.models import Review
from src.ingestion.csv_loader import ingest_csv
from src.models.sentiment import sentiment_analyzer

router = APIRouter()

class ReviewAnalysisRequest(BaseModel):
    text: str

class ReviewAnalysisResponse(BaseModel):
    text: str
    sentiment_score: float
    sentiment_label: str

@router.post("/ingest")
async def ingest_reviews(
    source_name: str,
    text_col: str,
    rating_col: str = None,
    timestamp_col: str = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint to ingest a CSV file of reviews into the database.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
        
    temp_file_path = f"data/raw/temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        inserted = ingest_csv(
            file_path=temp_file_path,
            db=db,
            source_name=source_name,
            text_col=text_col,
            rating_col=rating_col,
            timestamp_col=timestamp_col
        )
    except Exception as e:
        os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))
        
    os.remove(temp_file_path)
    return {"message": "Ingestion successful", "records_inserted": inserted}

@router.post("/analyze", response_model=ReviewAnalysisResponse)
async def analyze_single_review(request: ReviewAnalysisRequest):
    """
    Real-time analysis of a single review text payload.
    """
    result = sentiment_analyzer.analyze_text(request.text)
    return ReviewAnalysisResponse(
        text=request.text,
        sentiment_score=result["score"],
        sentiment_label=result["label"]
    )

@router.get("/analytics/sentiment-summary")
def get_sentiment_summary(db: Session = Depends(get_db)):
    """
    Aggregated metrics for the dashboard.
    """
    total_reviews = db.query(Review).count()
    if total_reviews == 0:
        return {"total_reviews": 0, "average_sentiment": 0.0}
        
    avg_sentiment = db.query(func.avg(Review.sentiment_score)).scalar() or 0.0
    return {
        "total_reviews": total_reviews,
        "average_sentiment": round(avg_sentiment, 4)
    }
