from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine
from models.todo_model import TodoModel, UserModel
from pydantic import BaseModel   
from typing import List

app = FastAPI()
# Create the database tables
TodoModel.metadata.create_all(bind=engine)
# Dependency to get the database session
def get_db():   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Pydantic model for request body
class TodoCreate(BaseModel):
    title: str
    description: str
    status: str
    completed: bool = False
# Pydantic model for response
class TodoResponse(TodoCreate):
    id: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str





# Create a new Todo
@app.post("/todos/{user_id}", response_model=TodoResponse)
async def create_todo(user_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoModel(title=todo.title, description=todo.description, status=todo.status, completed=todo.completed, user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Create a new User
@app.post("/create_user/")
async def create_user(todo: UserCreate, db: Session = Depends(get_db)):
    valid_user = UserModel(username = todo.username, email=todo.email, password=todo.password)
    db.add(valid_user)
    db.commit()
    db.refresh(valid_user)
    return valid_user


# Get all Todos
@app.get("/todos/")
async def get_todos(db: Session = Depends(get_db)):
    
    todos = db.query(TodoModel).all()
    return todos