from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from models import table_registry
engine = create_engine("sqlite:///todo.db", echo=True)
table_registry.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session