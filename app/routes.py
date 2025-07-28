from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import SentimentRequest
from .models import SentimentResult
from .services import analyze_sentiment, analyze_couples
from .database import SessionLocal
from app.s3_loader import load_csv_from_s3, save_to_db
from app.database import SessionLocal
from app.models import CoupleWellbeingTrend
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno del archivo .env

S3_KEY = os.getenv("S3_KEY", "training_dataset.csv")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
S3_BUCKET = os.getenv("S3_BUCKET", "api-modelo")

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
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/load-from-s3")
def load_s3_data():
    bucket = S3_BUCKET
    key = AWS_ACCESS_KEY_ID

    df = load_csv_from_s3(bucket, key="training_dataset.csv")
    save_to_db(df)

    return {"message": f"{len(df)} filas cargadas desde S3 a la base de datos"}

@router.get("/trends/")
def get_trends(couple_id: int):
    db: Session = SessionLocal()
    trends = db.query(CoupleWellbeingTrend)\
        .filter(CoupleWellbeingTrend.couple_id == couple_id)\
        .order_by(CoupleWellbeingTrend.week_number).all()

    result = [{
        "week": t.week_number,
        "stress": t.promedio_estres_individual,
        "sentiment": t.puntuacion_cuestionario_das,
        "communication": t.comunicacion_health_score,
        "churn_risk": t.churn_risk
    } for t in trends]

    return result

@router.get("/analyze-all")
def analyze_all(db: Session = Depends(get_db)):
    # Suponiendo que tienes una columna de texto en CoupleWellbeingTrend, por ejemplo 'descripcion'
    records = db.query(CoupleWellbeingTrend).all()
    results = []
    for r in records:
        # Si tienes una columna de texto, cámbiala aquí
        texto = getattr(r, "descripcion", None)
        if texto:
            label, score = analyze_sentiment(texto)
            results.append({
                "couple_id": r.couple_id,
                "week_number": r.week_number,
                "sentiment": label,
                "score": score
            })
    return results

@router.get("/couples-analysis")
def couples_analysis(db: Session = Depends(get_db)):
    return analyze_couples(db)
