from fastapi import HTTPException, status, UploadFile
from typing import List, Optional
from sqlalchemy.orm import Session
from models.assignments import Assignment
from schemas.assignments import  AssignmentUpdate
from services.assignment import assignment_service

class AssignmentCRUD:
    
    @staticmethod
    def get_assignment(db: Session, assignment_id: str):
        db_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not db_assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        return db_assignment
    
    @staticmethod
    def get_assignments(db: Session) -> List[Assignment]:
        return db.query(Assignment).all()
    @staticmethod
    def get_student_assignments(db: Session, student_id: str) -> List[Assignment]:
        return db.query(Assignment).filter(Assignment.student_id == student_id).all()
    @staticmethod
    def update_assignment(db: Session, assignment_id: str, assignment_update: AssignmentUpdate,  file: Optional[UploadFile] = None):
        db_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not db_assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        
        for key, value in assignment_update.model_dump(exclude_unset=True).items():
            if value is not None:
                if key == "student_name":
                    setattr(db_assignment, key, value.strip().lower())
                else: 
                    setattr(db_assignment, key, value)
        file_name = None
        if file:
            try:
                file_name = assignment_service.save_file(file)
                db_assignment.file_name = file_name
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"File upload failed: {e}")
        db.flush()
        db.refresh(db_assignment)
        return db_assignment
    @staticmethod
    def delete_assignment(db: Session, assignment_id: int):
        db_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not db_assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        
        db.delete(db_assignment)
        db.flush()
        return {"detail": "Assignment deleted successfully"}
    

assignment_crud = AssignmentCRUD()