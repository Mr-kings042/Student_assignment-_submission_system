from fastapi import HTTPException, status
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from models.teachers import Teacher
from models.assignments import Assignment, Comment, Like
from schemas.assignments import  CommentCreate, CommentUpdate, LikeCreate



class CommentCRUD:
    @staticmethod
    def add_comment(db: Session, comment: CommentCreate, assignment_id: str, teacher_id: str):
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
        db_comment = Comment(
            content=comment.content,
            assignment_id=assignment_id,
            teacher_id=teacher_id,
            created_at=datetime.utcnow(),
        )
        db.add(db_comment)
        db.flush()
        db.refresh(db_comment)
        return db_comment
    
    @staticmethod
    def update_comment(db: Session, comment_id: str, teacher_id: str, comment_update: CommentUpdate):
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        
        for key, value in comment_update.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(db_comment, key, value)
        
        db.flush()
        db.refresh(db_comment)
        return db_comment
    @staticmethod
    def get_comment_by_id(db: Session, comment_id: str):
        db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        return db_comment
    @staticmethod
    def get_comments_by_assignment_id(db: Session, assignment_id: str) -> List[Comment]:
        comments = db.query(Comment).filter(Comment.assignment_id == assignment_id).all()
        return comments
    @staticmethod
    def get_comments_by_teacher_id(db: Session, teacher_id: str) -> List[Comment]:
        comments = db.query(Comment).filter(Comment.teacher_id == teacher_id).all()
        return comments
    @staticmethod
    def get_all_comments(db: Session) -> List[Comment]:
        comments = db.query(Comment).all()
        return comments
    
    @staticmethod
    def delete_comment(db: Session, comment_id: str, teacher_id:str):
        db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        if db_comment.teacher_id != teacher_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this comment")
        db.delete(db_comment)
        db.flush()
        return {"detail": "Comment deleted successfully"}


comments_crud = CommentCRUD()