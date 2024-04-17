from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, UUID4

from uuid import uuid4

app = FastAPI()

class Question(BaseModel):
    """Schema for a question."""

    q_id: UUID4
    question: str
    answer: str | None


class QuestionCreate(BaseModel):
    """Schema for creating a new question. The user only needs to provide the question."""

    question: str


questions: list[Question] = []

@app.get("/")
def read_root():
    """Returns a simple message."""

    return {"message": "Hello World!"}

@app.get("/question")
def get_all_questions() -> list[Question]:
    """Returns all questions."""

    return questions

@app.post("/question", status_code=201)
def add_question(new_question: QuestionCreate) -> Question:
    """Adds a new question to the list of questions."""

    q_id = uuid4()

    created_question = Question(q_id=q_id, question=new_question.question, answer=None)
    questions.append(created_question)

    return created_question

@app.get("/question/{q_id}")
def get_question(q_id: UUID4) -> Question:
    """Returns a question by its id."""

    for question in questions:
        if question.q_id == q_id:
            return question

    raise HTTPException(404, f"Question with id {q_id} not found!")

@app.put("/question/{q_id}")
def update_question(q_id: UUID4, updated_question: QuestionCreate) -> Question:
    """Updates a question by its id."""

    for question in questions:
        if question.q_id == q_id:
            question.question = updated_question.question
            return question

    raise HTTPException(404, f"Question with id {q_id} not found!")

@app.delete("/question/{q_id}")
def delete_question(q_id: UUID4) -> Question:
    """Deletes a question by its id."""

    for i, question in enumerate(questions):
        if question.q_id == q_id:
            del questions[i]
            return question

    raise HTTPException(404, f"Question with id {q_id} not found!")

@app.post("/question/{q_id}/answer")
def add_answer(q_id: UUID4, answer: str) -> Question:
    """Adds an answer to a question by its id."""

    for question in questions:
        if question.q_id == q_id:
            question.answer = answer
            return question

    raise HTTPException(404, f"Question with id {q_id} not found!")