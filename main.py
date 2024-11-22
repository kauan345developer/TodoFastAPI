from typing import Union

from fastapi import FastAPI
from schemas import TodoCreate
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Todo
from database import get_session


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/todo/",response_model=TodoCreate)
def todo_create(
    todo: TodoCreate, session: Session = Depends(get_session), 
):
    todo = Todo(title=todo.title, description=todo.description)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@app.get("/todos/")
def todo_list(session: Session = Depends(get_session)):
    todos = session.scalars(select(Todo)).all()
    return todos
  
@app.get("/todo/{todo_id}")
def todo(todo_id:int,session: Session = Depends(get_session)):
  todo = session.scalar(select(Todo).where(Todo.id == todo_id))
  return todo

