from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()
# Load environment variables from .env file
print(os.getenv("DB_URI"))

def get_db_client():
    try:
        client = MongoClient(os.getenv("DB_URI"))
        print("Connected to the database")
        return client
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

client = get_db_client()
db = client["fastapidb"] # type: ignore





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
            "error": None,
            "message": "Todos read successfully",
            "status": "success"
            }
    except Exception as e:
        print(f"Error reading todos: {e}")
        return {
            "data": [],
            "error": "Error reading todos",
            "message": str(e),
            "status": "failed"
            }
