from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field
from transformers import pipeline
from typing import List


app = FastAPI()
sentiment = pipeline(
    task="sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


class Replica(BaseModel):
    text: str = Field(min_length=8, max_length=32)
    speaker: str


class DialogRequestModel(BaseModel):
    dialog: List[Replica] = Field(min_items=2, max_items=8)


class Labels(Enum):
    positive = "POSITIVE"
    negative = "NEGATIVE"
    neutral = "NEUTRAL"


class DialogResponseModel(BaseModel):
    labels: List[Labels]
    class Config:  
        use_enum_values = True


@app.post("/api/v1/sent")
def get_sentiment(drm: DialogRequestModel) -> DialogResponseModel:
    sentences = [replica.text for replica in drm.dialog]
    output = sentiment(sentences)
    labels = [item["label"] for item in output]
    return DialogResponseModel(labels=labels)
