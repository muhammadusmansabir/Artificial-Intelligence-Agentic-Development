from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int

@app.post("/user/{id}")
def create_user(user: User, id: int, query: Optional[str] = None):
    try:
        return {
            "status": "success",
            "data":{
                "user": user,
                "query": query,
                "id": id


            } 
            }           
    except Exception as e:
        print(e)        
        return {
            "status": "error",
            "error": str(e)
        }
   




@app.get("/")
def get_hello_world2():
    return {"Hello": "auth"}


#path parameter
@app.get("/user/{id}/{username}")
def get_user(id, username):
    try:
        return {
            "data":{
                "id": id, 
                "username": username,
                "profile_url": "https://github.com/muhammadusmansabir",
                "email": "user@example.com",

            },
            "status": "success"
            }
    except Exception as e:
        print(e)
        return {"error": str(e)}


#query parameter
@app.get("/search")
def get_search(id: int, name: str, query: str):
    return {
        "query": query, 
        "name": name,
        "id": id,
    
        }
    
#body parameter
@app.post("/bodyparameter")
def get_hello_world():
    return {"Hello": "body parameter"}

@app.post("/login")
def get_hello_world():
    print("Function Call!")
    return {"Hello": "login post"}


@app.delete("/login")
def get_hello_world23():
    print("Function Call!")
    return {"Hello": "login delete"}

@app.put("/login")
def get_hello_world232():
    print("Function Call!")
    return {"Hello": "login put"}

@app.get("/auth/signup")
def get_hello_world1():
    return {"Hello": "signup"}
