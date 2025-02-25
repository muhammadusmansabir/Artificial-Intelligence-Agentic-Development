# Poetry add python-multipart
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles # type: ignore

import shutil
import os

#UPLOAD_DIRECTORY = "03-fastapi/uploads"  #define upload directory
current_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIRECTORY = os.path.join(current_dir, "uploads")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True) #create directory if not exists

app = FastAPI()

#mount the upload dir
# ectory to serve static files
app.mount("/static", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploads")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #Return public url to access the file
    file_url = f"/static/{file.filename}"

    return {"filename": file.filename, "url": file_url}