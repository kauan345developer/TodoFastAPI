from typing import Union

from fastapi import FastAPI
from schemas import TodoCreate,TodoEdit
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select, update
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

@app.patch("/todo/{todo_id}")
def todo_edit(todo_id:int,todo:TodoEdit,session: Session = Depends(get_session)):
    
    db_todo = session.scalar(
        select(Todo).where(Todo.id == todo_id)
    )
    
    # if not todo:
    #     raise HTTPException(
    #         status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
    #     )
    # print(todo.model_dump())
    # print(**todo.model_dump())
    
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    # query = update(Todo).where(Todo.id == todo_id).values(Todo(title=todo.title, description=todo.description))
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.delete("/todo/{todo_id}")
def todo_delete(todo_id:int,session: Session = Depends(get_session)):
    db_todo = session.scalar(
        select(Todo).where(Todo.id == todo_id)
    )
    
    session.delete(db_todo)
    session.commit()
    
    return {'message': 'Task has been deleted successfully.'}

