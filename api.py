from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    question: str
    answer: str | None
    id: int

@app.get("/api/question", description="Get all questions")
def read_questions() -> list[Question]:
    return [Question(question="What is the capital of France?", answer="Paris", id=1),]

@app.get("/api/question/{question_id}")
def read_question(question_id: int) -> Question:
    return Question(question="What is the capital of France?", answer="Paris", id=question_id)

@app.post("/api/question")
def create_question(question: Question) -> Question:
    return question

@app.put("/api/question/{question_id}")
def update_question(question_id: int, question: Question) -> Question:
    return question

@app.delete("/api/question/{question_id}")
def delete_question(question_id: int) -> None:
    return None
