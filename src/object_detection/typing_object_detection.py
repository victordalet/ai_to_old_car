from typing import List, Dict
from pydantic import BaseModel


class BoxDetection(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class JsonDetection(BaseModel):
    name: str
    confidence: float
    box: BoxDetection
