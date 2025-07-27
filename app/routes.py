from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import SentimentRequest
from .models import SentimentResult
from .services import analyze_sentiment
from .database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/analyze")
def analyze_sentiment_route(payload: SentimentRequest, db: Session = Depends(get_db)):
    try:
        label, score = analyze_sentiment(payload.text)

        result = SentimentResult(
            source_type=payload.source_type,
            source_id=payload.source_id,
            client_id=payload.client_id,
            sentiment_score=score,
            sentiment_label=label,
        )
        db.add(result)
        db.commit()
        return {"message": "Sentiment analyzed", "label": label, "score": score}
    except Exception as e:
        # Esto te dará el error en la respuesta y en los logs
        raise HTTPException(status_code=500, detail=str(e))
