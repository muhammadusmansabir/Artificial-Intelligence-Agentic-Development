from fastapi import FastAPI 
from routes.posts_routes import postsRouter
from routes.auth_routes import authRouter

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server is running"}


app.include_router(authRouter, prefix="/auth", tags=["auth"])
app.include_router(postsRouter, prefix="/posts", tags=["posts"])