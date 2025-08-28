import shutil
from fastapi import HTTPException, status, UploadFile
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models.students import Student
from models.assignments import Assignment, Like
from schemas.assignments import AssignmentCreate, LikeCreate


class AssignmentService:
    @staticmethod
    def save_file(file: UploadFile) -> str:
        upload_dir = Path("uploads/assignments")
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.filename
        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"File upload failed: {e}")
        finally:
            file.file.close()
        return file.filename

    @staticmethod
    def submit_assignment(db: Session, assignment: AssignmentCreate, student_id: str, file: Optional[UploadFile] = None):
        # Query for the student by their ID
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID {student_id} not found",
            )

        # Verify that the provided student name matches the name in the database for that ID.
        if student.name != assignment.student_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Provided student name '{assignment.student_name}' does not match the name for the given student ID.",
            )
        file_name = None
        if file:
            try:
                file_name = AssignmentService.save_file(file)
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"File upload failed: {e}")
        db_assignment = Assignment(
            title=assignment.title,
            subject=assignment.subject,
            description=assignment.description,
            file_name=file_name,
            student_id=student.id,
            student_name=student.name.strip().lower(),
            is_submitted=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(db_assignment)
        db.flush()
        db.refresh(db_assignment)
        return db_assignment

    @staticmethod
    def add_like(db: Session, like: LikeCreate, assignment_id: int):
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        existing_like = db.query(Like).filter(Like.assignment_id == assignment_id, Like.teacher_id == like.teacher_id).first()
        if existing_like:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Like already exists by this teacher for the assignment")
        db_like = Like(**like.model_dump())
        db.add(db_like)
        db.flush()
        db.refresh(db_like)
        return db_like
    

assignment_service = AssignmentService()