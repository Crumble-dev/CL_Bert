from sqlalchemy import Column, BigInteger, Integer, Float, String, Enum, TIMESTAMP
from .database import Base
import enum

class SourceType(str, enum.Enum):
    EMOTIONAL_LOG = "EMOTIONAL_LOG"
    TASK_COMMENT = "TASK_COMMENT"

class SentimentResult(Base):
    __tablename__ = "sentiment_results"

    id = Column(BigInteger, primary_key=True, index=True)
    source_type = Column(Enum(SourceType), nullable=False)
    source_id = Column(BigInteger, nullable=False)
    client_id = Column(Integer, nullable=False)
    sentiment_score = Column(Float, nullable=False)
    sentiment_label = Column(String(50), nullable=False)
    analyzed_at = Column(TIMESTAMP)

class CoupleWellbeingTrend(Base):
    __tablename__ = "couple_wellbeing_trends"

    id = Column(Integer, primary_key=True, autoincrement=True)
    couple_id = Column(Integer, nullable=False)
    week_number = Column(Integer, nullable=False)

    puntuacion_cuestionario_das = Column(Float)
    calificacion_satisfaccion_tareas_avg = Column(Float)
    tasa_cumplimiento_tareas = Column(Float)
    promedio_estres_individual = Column(Float)
    interacion_balance_ratio = Column(Float)
    empatia_gap_score = Column(Float)
    comunicacion_health_score = Column(Float)

    churn_risk = Column(Integer)

    # Embeddings de ejemplo
    embedding_0 = Column(Float)
    embedding_1 = Column(Float)
    embedding_2 = Column(Float)
    embedding_3 = Column(Float)
    embedding_4 = Column(Float)
    embedding_5 = Column(Float)
    embedding_6 = Column(Float)
    embedding_7 = Column(Float)
    embedding_8 = Column(Float)
    embedding_9 = Column(Float)
    embedding_10 = Column(Float)

