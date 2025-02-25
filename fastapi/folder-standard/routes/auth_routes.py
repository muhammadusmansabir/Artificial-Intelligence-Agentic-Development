from fastapi import APIRouter

authRouter = APIRouter()

@authRouter.get("/register")
def register():
    return {"message": "Register"}

@authRouter.get("/login")   
def login():
    return {"message": "Login"}

@authRouter.get("/logout")   
def logout():       
    return {"message": "Logout"}

@authRouter.get("/forget-password")   
def forget_password():  
    return {"message": "Forget Password"}