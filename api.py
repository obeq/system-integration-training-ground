from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, UUID4

import requests
from dotenv import load_dotenv
import os
load_dotenv()

from uuid import uuid4

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBasic()

OPENAI_URL="https://api.openai.com/v1/chat/completions"
# openai_key = dotenv.get_variable('.env', "OPENAI_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")

class User(BaseModel):
    username: str
    email: str | None = None


class Question(BaseModel):
    """Schema for a question."""

    q_id: UUID4
    question: str
    answer: str | None


class QuestionCreate(BaseModel):
    """Schema for creating a new question. The user only needs to provide the question."""

    question: str


questions: list[Question] = []

# def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
#     """Returns the current user."""

#     return User(username=token + "user", email=token + "@example.com")

def get_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> User:
    """Returns the current user."""

    return User(username=credentials.username, email=credentials.username + "@example.com")


def get_answer_from_ai(question_text: str) -> str:
    """Returns an answer from an AI model."""

    headers = {
        'Authorization': f'Bearer {OPENAI_KEY}',
        'Content-Type': 'application/json'
    }

    # Data to be sent (query)
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Du är en tålmodig lärare som alltid är beredd med ett svar."
            },
            {
                "role": "user",
                "content": question_text
            }
        ]
    }

    # Making the POST request
    response = requests.post(OPENAI_URL, headers=headers, json=data)

    if (response.status_code != 200):
        return "Sorry, I don't know the answer to that question."
    
    results = response.json()

    return results["choices"][0]["message"]["content"]

@app.get("/")
def read_root():
    """Returns a simple message.
    
    This message is unexpected, but it is a good message."""

    return {"message": "Hello World!"} # This is a comment

@app.get("/question")
def get_all_questions() -> list[Question]:
    """Returns all questions."""

    return questions

@app.post("/question", status_code=201)
def add_question(new_question: QuestionCreate, current_user: Annotated[User, Depends(get_current_user)]) -> Question:
    """Adds a new question to the list of questions."""

    unique_id = uuid4()

    ai_answer = get_answer_from_ai(new_question.question)

    created_question = Question(
        q_id=unique_id,
        question=new_question.question,
        answer=ai_answer
    )
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

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return {"access_token": form_data.username[::-1], "token_type": "bearer"}