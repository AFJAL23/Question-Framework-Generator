from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from engine import generate_question

app = FastAPI(
    title="Task 09 Question Generator API",
    description="Domain based intelligent question generation system",
    version="2.0.0"
)


class QuestionRequest(BaseModel):
    domain: str = Field(..., min_length=2)
    difficulty: str = Field(..., min_length=4)
    previous_context: List[str] = []


@app.get("/")
def home():
    return {
        "message": "Task 09 Question Generation API Running",
        "status": "success",
        "version": "2.0.0"
    }


@app.post("/generate-question")
def get_question(data: QuestionRequest):

    result = generate_question(
        data.domain,
        data.difficulty,
        data.previous_context
    )

    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )

    return {
        "status": "success",
        "data": result
    }