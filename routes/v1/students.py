from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.students import StudentCreate, StudentUpdate, StudentResponse
from crud.students import student_crud
from typing import List

student_router = APIRouter()

@student_router.post("/", status_code=status.HTTP_201_CREATED, response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    try:
        student = student_crud.create_student(db, student)
        db.commit()
        return student
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

@student_router.get("/{student_id}", status_code=status.HTTP_200_OK, response_model=StudentResponse)
def get_student(student_id: UUID, db: Session = Depends(get_db)):
      try:
        student = student_crud.get_student(db, student_id)
       
        return student
      except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
      

@student_router.get("/", status_code=status.HTTP_200_OK, response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    try:
        students = student_crud.get_students(db)
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@student_router.patch("/{student_id}", status_code=status.HTTP_200_OK, response_model=StudentResponse)
def update_student(student_id: UUID, student_update: StudentUpdate, db: Session = Depends(get_db)):
    try:
        student = student_crud.update_student(db, student_id, student_update)
        db.commit()
        return student
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

@student_router.delete("/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(student_id: UUID, db: Session = Depends(get_db)):
    try:
        student_crud.delete_student(db, student_id)
        db.commit()
        return {"detail": "Student deleted successfully"}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
        
