from fastapi import FastAPI

from pydantic import BaseModel , Field
from typing import Any

app = FastAPI(title= "text summerizer api")

class SummerizeRequest(BaseModel): 
    text : str = Field(min_length=20, max_length=10000)
    max_sentence: int = Field(default= 2 , ge=1, le=10)

@app.get("/health")
def health_check():
    return {"status" : "healthy"}


@app.post("/summarize")
def summarize(request: SummerizeRequest) -> dict[str, Any]:
    sentences = [
        sentence.strip()
        for sentence in request.text.split(".")
        if sentence.strip()
    ]

    summary = ". ".join(sentences[:request.max_sentence])

    if summary:
        summary += "."

    return {
        "summary": summary,
        "original_length": len(request.text),
        "summary_length": len(summary),
    }
