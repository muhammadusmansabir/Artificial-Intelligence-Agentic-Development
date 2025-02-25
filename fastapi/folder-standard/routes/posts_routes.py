from fastapi import APIRouter
from utils.post_utility import post_data
postsRouter = APIRouter()

@postsRouter.get("/")   
def get_posts():
    return {"message": "Get all posts"}

@postsRouter.get("/{post_id}")
def get_post(post_id: int):
    data = post_data(post_id)
    print(data)
    return {"message": f"Get post with id: {post_id}"}

@postsRouter.post("/create")
def create_post():
    return {"message": "Create post"}

@postsRouter.put("update/{post_id}")
def update_post(post_id: int):
    return {"message": f"Update post with id: {post_id}"}

@postsRouter.delete("delete/{post_id}")   
def delete_post(post_id: int):  
    return {"message": f"Delete post with id: {post_id}"}