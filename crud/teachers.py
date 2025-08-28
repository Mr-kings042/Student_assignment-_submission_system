from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.teachers import Teacher
from schemas.teachers import TeacherCreate, TeacherUpdate, TeacherResponse


class TeacherCRUD:
    @staticmethod
    def create_teacher(db: Session, teacher: TeacherCreate):
        db_teacher = Teacher(
            name=teacher.name.strip().lower(),
            email=teacher.email,
        )
        db.add(db_teacher)
        db.flush()
        db.refresh(db_teacher)
        return db_teacher

    @staticmethod
    def get_teacher(db: Session, teacher_id: int):
        return db.query(Teacher).filter(Teacher.id == teacher_id).first()

    @staticmethod
    def get_teacher_by_email(db: Session, email: str):
        return db.query(Teacher).filter(Teacher.email == email).first()

    @staticmethod
    def get_teachers(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Teacher).all()

    @staticmethod
    def update_teacher(db: Session, teacher_id: int, teacher: TeacherUpdate):
        db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not db_teacher:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        
        for key, value in teacher.model_dump(exclude_unset=True).items():
            if value is not None:
               if key == "name":
                   setattr(db_teacher, key, value.strip().lower())
               else:
                   setattr(db_teacher, key, value)
        
        db.flush()
        db.refresh(db_teacher)
        return db_teacher

    @staticmethod
    def delete_teacher(db: Session, teacher_id: int):
        db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not db_teacher:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        db.delete(db_teacher)
        db.flush()
        return {"message": "Teacher deleted successfully"}
    

teacher_crud = TeacherCRUD()
