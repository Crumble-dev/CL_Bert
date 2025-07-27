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
