from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.teachers import TeacherCreate, TeacherUpdate, TeacherResponse
from crud.teachers import teacher_crud
from models.teachers import Teacher
from typing import List

teacher_router = APIRouter()

@teacher_router.post("/", status_code=status.HTTP_201_CREATED, response_model=TeacherResponse)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    try:
        teacher = teacher_crud.create_teacher(db, teacher)
        db.commit()
        return teacher
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@teacher_router.get("/{teacher_id}", status_code=status.HTTP_200_OK, response_model=TeacherResponse)
def get_teacher(teacher_id: UUID, db: Session = Depends(get_db)):
    try:
        teacher = teacher_crud.get_teacher(db, teacher_id)
        if not teacher:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        return teacher
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@teacher_router.get("/", status_code=status.HTTP_200_OK, response_model=List[TeacherResponse])
def get_teachers(db: Session = Depends(get_db)):
    try:
        teachers = teacher_crud.get_teachers(db)
        return teachers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@teacher_router.patch("/{teacher_id}", status_code=status.HTTP_200_OK, response_model=TeacherResponse)
def update_teacher(teacher_id: UUID, teacher_update: TeacherUpdate, db: Session = Depends(get_db)):
    try:
        teacher = teacher_crud.update_teacher(db, teacher_id, teacher_update)
        db.commit()
        return teacher
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@teacher_router.delete("/{teacher_id}", status_code=status.HTTP_200_OK)
def delete_teacher(teacher_id: UUID, db: Session = Depends(get_db)):
    try:
        teacher_crud.delete_teacher(db, teacher_id)
        db.commit()
        return {"detail": "Teacher deleted successfully"}
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))