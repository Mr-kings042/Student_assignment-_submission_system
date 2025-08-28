from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.students import Student
from schemas.students import StudentCreate, StudentUpdate, StudentResponse


class StudentCRUD:
    @staticmethod
    def create_student(db: Session, student: StudentCreate) -> StudentResponse:
        existing_email = db.query(Student).filter(Student.email == student.email).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        db_student = Student(
            name=student.name.strip().lower(),
            email=student.email,
        )
        db.add(db_student)
        db.flush()
        db.refresh(db_student)
        return db_student

    @staticmethod
    def get_student(db: Session, student_id: str):
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        return db_student

    @staticmethod
    def get_students(db: Session) -> list[StudentResponse]:
        students = db.query(Student).all()
        return students

    @staticmethod
    def update_student(db: Session, student_id: str, student_update: StudentUpdate) -> StudentResponse:
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        
        for key, value in student_update.model_dump(exclude_unset=True).items():
            if value is not None:
                if key == "name":
                   setattr(db_student, key, value.strip().lower())
                else:
                  setattr(db_student, key, value)
                
        
        db.flush()
        db.refresh(db_student)
        return db_student

    @staticmethod
    def delete_student(db: Session, student_id: str) -> None:
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        
        db.delete(db_student)
        db.commit()
        return {"detail": "Student deleted successfully"}
    

student_crud = StudentCRUD()