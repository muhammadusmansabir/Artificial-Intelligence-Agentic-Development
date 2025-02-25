from fastapi import FastAPI, APIRouter

app = FastAPI()
postRouter = APIRouter()


@app.get("/")   
def get_posts():
    return {"posts": "app posts"}

@postRouter.get("/")   
def get_posts():
    return {"posts": "router posts get"}

@postRouter.get("/create")
def create_post():
    return {"post": "router post create"} 

@postRouter.get("/likes")
def get_likes():
    return {"likes": "router post likes"}

app.include_router(postRouter, prefix="/posts", tags=["posts"])

