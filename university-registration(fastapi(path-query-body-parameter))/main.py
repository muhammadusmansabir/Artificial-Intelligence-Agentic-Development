

from http.client import HTTPException
from fastapi import FastAPI, Query # type: ignore
from typing import Optional
from pydantic import BaseModel, EmailStr, conlist, conint # type: ignore


app = FastAPI()


@app.get("/student/{student_id}")

def student_info(student_id: int, include_grades: bool = False, semester: Optional[str] = Query(None, regex="^(Fall|Spring|Summer)\\d{4}$")):
    try:
        # Check if the student_id is within the valid range
        if student_id > 1000 and student_id < 9999:
            if include_grades:
                # If include_grades is True, return the student's grades
                return {
                    "status": "ok",
                    "data": {
                        "student_id": student_id,
                        "grades": {
                            "semester": semester,
                            "grade": "A"
                        }

                    }
                }
            else:
                # If include_grades is False, return the student's basic information
              return {
                "status": "ok",
                "data": {
                    "student_id": student_id
                }
                }
        else:
            # Raise an HTTPException if the student ID is not in the valid range
            raise ValueError("Student ID is not between 1000 and 9999/Grades are not available against this ID")
            
            
    except ValueError as e:
        # Catch the ValueError and handle it in the except block
        print(f"Error: {e}")
        return {"error": str(e)}



class Student(BaseModel):
    name: str = Query(regex=r'^[A-Za-z ]{1,50}$')
    email: EmailStr
    age: conint(ge=18, le=30) # type: ignore
    courses: conlist(str, min_length=1, max_length=5) # type: ignore



@app.post("/student/register")
def register_student(student: Student):
   
        return {    
                "status": "OK",
                 "data": student
                 }

 
class Student_Email(BaseModel):
    email: EmailStr

@app.put("/student/{student_id}/email")
def update_student(student_id: conint(ge=1000, le=9999), student_email: Student_Email): # type: ignore
    
         
         
        try:    
            return {
                "status": "OK",
                 "data": {
                     "student_id": student_id,
                     "student_email": student_email
                 }  
                 }
        except Exception as e:
               
            return {
            "status": "error",
            "error": str(e)
            }


