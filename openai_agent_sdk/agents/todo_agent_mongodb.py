import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool
from pymongo import MongoClient
from bson import ObjectId

# Load .env
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
mongo_uri = os.getenv('MONGO_URI')  # Example: mongodb://localhost:27017 or Atlas URI

# Mongo client setup with connection check
try:
    mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
    mongo_client.admin.command('ping')
    print("✅ MongoDB connection successful.")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    exit(1)

db = mongo_client["todoDB"]
todos_collection = db["todos"]

# Gemini client setup
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Tools

@function_tool
def create_todo(task: str, status: str = "pending") -> dict:
    """Create a new todo item"""
    todo = {"task": task, "status": status}
    result = todos_collection.insert_one(todo)
    return {"message": "Todo created", "id": str(result.inserted_id)}

@function_tool
def get_todos() -> list:
    """Fetch all todos"""
    todos = list(todos_collection.find())
    return [{"id": str(todo["_id"]), "task": todo["task"], 
             "status": todo["status"]} for todo in todos]

@function_tool
def update_todo(todo_id: str, task: str = None, status: str = None) -> dict:
    """Update an existing todo"""
    update_fields = {}
    if task: update_fields["task"] = task
    if status: update_fields["status"] = status
    result = todos_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": update_fields})
    if result.matched_count:
        return {"message": "Todo updated"}
    else:
        return {"error": "Todo not found"}

@function_tool
def delete_todo(todo_id: str) -> dict:
    """Delete a todo by ID"""
    result = todos_collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count:
        return {"message": "Todo deleted"}
    else:
        return {"error": "Todo not found"}

# Agent setup
agent = Agent(
    name="Todo Agent",
    instructions="You are a helpful assistant for managing todos. You can create, list, update, and delete tasks using MongoDB.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[create_todo, get_todos, update_todo, delete_todo],
)
while True:
    # Agent interaction
    query = input("What do you want to do with your todos? ")
    result = Runner.run_sync(agent, query)
    print("🧠 Agent Response:\n", result.final_output)

    # Exit condition
    if "exit" in query.lower():
        break
