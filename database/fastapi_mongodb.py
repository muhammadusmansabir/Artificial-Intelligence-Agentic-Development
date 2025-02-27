from fastapi import FastAPI
from pymongo import MongoClient # type: ignore
from dotenv import load_dotenv
from bson import ObjectId # type: ignore
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI()

load_dotenv()
# Load environment variables from .env file
print(os.getenv("DB_URI"))
def db_get_client():
    try:
        MONGO_URI = os.getenv("DB_URI")
        client = MongoClient(MONGO_URI)
        print("Connected to MongoDB")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


client = db_get_client()
db = client["fastapidb"]
#collection = db["todos"]



@app.get("/")
def read_root():
    return {"status": "Server is running"}

@app.get("/todos")
def read_todos():
    try:
        todos = db.todos.find()
        listTodos = []
        for todo in todos:
            listTodos.append({
                "id": str(todo["_id"]),
                "title": todo["title"],
                "description": todo["description"],
                "status": todo["status"],
                "created_at": todo["created_at"],
            })
        return {
            "data": listTodos,
            "status": "success",
            "message": "Todos fetched successfully",
            "code": 200,
            "error": None
             
            }
    except Exception as e:
        return {
            "todos": [],
            "status": "failed",
            "message": "Error fetching todos",
            "error": str(e)
            }   
   
@app.get("/todos/{id}")
def read_todo_by_id(id: str):
    try:
        todo = db.todos.find_one({"_id": ObjectId(id)})
        if todo is None:
            return {
                "data": {},
                "status": "failed",
                "message": "Todo not found",
                "code": 404,
                "error": None
            }
        return {
            "data": {
                "id": str(todo["_id"]),
                "title": todo["title"],
                "description": todo["description"],
                "status": todo["status"],
                "created_at": todo["created_at"],
            },
            "status": "success",
            "message": "Todo fetched successfully",
            "code": 200,
            "error": None
            }     
    except Exception as e:
        return {
            "todos": [],
            "status": "failed",
            "message": "Error fetching todo",
            "error": str(e)
        }
    
@app.get("/fetch_todos_by_title")
def read_todo_by_title(title: str):
    try:
        todo = db.todos.find_one({"title": title})
        if todo is None:
            return {
                "data": {},
                "status": "failed",
                "message": "Todo not found",
                "code": 404,
                "error": None
            }
        return {
            "data": {
                "id": str(todo["_id"]),
                "title": todo["title"],
                "description": todo["description"],
                "status": todo["status"],
                "created_at": todo["created_at"],
            },
            "status": "success",            
            "message": "Todo fetched successfully",            
            "code": 200,
            "error": None   
            }     
    except Exception as e:
        return {
            "todos": [],
            "status": "failed",
            "message": "Error fetching todo",
            "error": str(e)
        }
    
class Todo(BaseModel):
    title: str
    description: str
    status: str

@app.post("/create_todos")
def create_todo(todo: Todo):
    try:
        result = db.todos.insert_one({
            "title": todo.title,
            "description": todo.description,
            "status": todo.status,
            "created_at": str(datetime.now())
        })
    
        return {
            "data":{
                "id": str(result.inserted_id),
            },
            "status": "success",
            "message": "Todo created successfully",
            "code": 200,
            "error": None
        }
    except Exception as e:
        return {
            "data": {},
            "status": "failed",
            "message": "Error creating todo",
            "error": str(e)
        }
    
@app.delete("/delete_todo/{id}")
def delete_todo(id: str):
    try:
        result = db.todos.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return {
                "data": {},
                "status": "failed",
                "message": "Todo not found",
                "code": 404,
                "error": None
            }   
        return {
            "data": {},
            "status": "success",
            "message": "Todo deleted successfully",
            "code": 200,
            "error": None
        }       
    except Exception as e:
        return {
            "data": {},
            "status": "failed",
            "message": "Error deleting todo",
            "error": str(e)
        }
    
@app.put("/update_todo/{id}")
def update_todo(id: str, todo: Todo):
    try:
        result = db.todos.update_one({"_id": ObjectId(id)}, {"$set": {
            "title": todo.title,
            "description": todo.description,
            "status": todo.status,
            "created_at": str(datetime.now())
        }})
        if result.matched_count == 0:
            return {
                "data": {},
                "status": "failed",
                "message": "Todo not found",
                "code": 404,
                "error": None
            }
        return {
            "data": {},
            "status": "success",
            "message": "Todo updated successfully",
            "code": 200,
            "error": None
        }       
    except Exception as e:
        return {
            "data": {},
            "status": "failed",
            "message": "Error updating todo",
            "error": str(e)
        }