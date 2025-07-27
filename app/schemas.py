from pydantic import BaseModel
from enum import Enum

class SourceType(str, Enum):
    EMOTIONAL_LOG = "EMOTIONAL_LOG"
    TASK_COMMENT = "TASK_COMMENT"

class SentimentRequest(BaseModel):
    source_type: SourceType
    source_id: int
    client_id: int
    text: str
