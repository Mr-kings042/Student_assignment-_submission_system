from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile,Form, File, status
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.assignments import AssignmentCreate, AssignmentUpdate, AssignmentResponse, CommentCreate, CommentResponse, CommentUpdate, LikeCreate
from crud.assignment import assignment_crud
from services.assignment import assignment_service
from typing import List, Optional

assignment_router = APIRouter()

@assignment_router.post("/{student_id}/submit",status_code=status.HTTP_201_CREATED, response_model=AssignmentResponse)
def submit_assignment( 
    student_id: UUID,
    title: str = Form(...),
    subject: str = Form(...),
    description: str = Form(...),
    student_name: str = Form(...), 
    file: Optional[UploadFile]= File(None), 
    db: Session = Depends(get_db)):
    try:
        assignment_data = AssignmentCreate(
            title=title,
            subject=subject,
            description=description,
            student_name=student_name  
        )
        assignment = assignment_service.submit_assignment(db, assignment_data,student_id, file)
        db.commit()
        return assignment
    except HTTPException as e:
        db.rollback()
        # For any other unexpected errors, return a generic 500
        raise HTTPException(status_code=500, detail=str(e))

@assignment_router.get("/{assignment_id}", status_code=status.HTTP_200_OK, response_model=AssignmentResponse)
def get_assignment(assignment_id: UUID, db: Session = Depends(get_db)):
    try:
        assignment = assignment_crud.get_assignment(db, assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        return assignment
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
@assignment_router.get("/", status_code=status.HTTP_200_OK, response_model=List[AssignmentResponse])
def get_assignments(db: Session = Depends(get_db)):
    try:
        assignments = assignment_crud.get_assignments(db)
        return assignments
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
@assignment_router.get("/{student_id}/assignments", status_code=status.HTTP_200_OK, response_model=List[AssignmentResponse])
def get_student_assignments(student_id: UUID,db: Session = Depends(get_db)):
    try:
        assignments = assignment_crud.get_student_assignments(db, student_id)
        return assignments
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@assignment_router.patch("/{assignment_id}", status_code=status.HTTP_200_OK, response_model=AssignmentResponse)
def update_assignment(assignment_id: UUID,  title: str = Form(None),
    description: str = Form(None),
    subject: str = Form(None),
    student_name: str = Form(None),
    
    db: Session = Depends(get_db), file: Optional[UploadFile] = File(None)):
    try:
        assignment_update = AssignmentUpdate(
            title=title,
            subject=subject,
            description=description,
            student_name=student_name,
            
        )
        assignment = assignment_crud.update_assignment(db, assignment_id, assignment_update, file)
        db.commit()
        return assignment
    except HTTPException as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@assignment_router.delete("/{assignment_id}", status_code=status.HTTP_200_OK)
def delete_assignment(assignment_id: UUID, db: Session = Depends(get_db)):
    try:
        assignment_crud.delete_assignment(db, assignment_id)
        db.commit()
        return {"detail": "Assignment deleted successfully"}
    except HTTPException as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



