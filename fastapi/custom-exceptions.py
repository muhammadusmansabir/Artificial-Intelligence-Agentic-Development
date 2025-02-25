from fastapi import HTTPException, FastAPI, File, UploadFile
from fastapi.responses import JSONResponse # type: ignore
from fastapi.exceptions import RequestValidationError # type: ignore
from fastapi import Request

app = FastAPI()

@app.exception_handler(RequestValidationError) # type: ignore
async def validation_exception_handler(request: Request, exc: RequestValidationError): # type: ignore
    errors = []
    for error in exc.errors():
     errors.append({
        "field": ".".join(map(str, error["loc"])),
        "message": error["msg"]
    })

    return JSONResponse(
        status_code=400, 
         content= {
             "message": "Validation Error",
            "status": "error",
            "error": errors
            }
         )

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)): 
    return {"filename": file.filename}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str):  
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}