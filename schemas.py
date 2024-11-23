from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    description: str

class TodoEdit(BaseModel):
    title: str | None = None
    description: str | None = None
    