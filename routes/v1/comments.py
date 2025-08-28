from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile,Form, File, status
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.assignments import  CommentCreate, CommentResponse, CommentUpdate, LikeCreate
from crud.comments import comments_crud
from services.assignment import assignment_service
from typing import List, Optional

comments_router = APIRouter()



@comments_router.post("/{assignment_id}/comments/{teacher_id}", status_code=status.HTTP_201_CREATED, response_model=CommentResponse)
def add_comment(assignment_id: UUID, teacher_id: UUID, content:str = Form(...), db: Session = Depends(get_db)):
    try:
        comment = CommentCreate(content=content)
        comment = comments_crud.add_comment(db, comment, assignment_id, teacher_id)
        db.commit()
        return comment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@comments_router.patch("/{comment_id}/{teacher_id}", status_code=status.HTTP_200_OK, response_model=CommentResponse)
def update_comment(comment_id: UUID, teacher_id:UUID, comment_update: CommentUpdate, db: Session = Depends(get_db)):
    try:
        comment = comments_crud.update_comment(db, comment_id,teacher_id, comment_update)
        db.commit()
        return comment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@comments_router.get("/{comment_id}/comment", status_code=status.HTTP_200_OK, response_model=CommentResponse)
def get_comment(comment_id: UUID, db: Session = Depends(get_db)):
    try:
        comment = comments_crud.get_comment_by_id(db, comment_id)
        return comment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@comments_router.get("/", status_code=status.HTTP_200_OK, response_model=List[CommentResponse])
def get_all_comments(db: Session = Depends(get_db)):
    try:
        comments = comments_crud.get_all_comments(db)
        return comments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@comments_router.get("/assignments/{assignment_id}/comments", status_code=status.HTTP_200_OK, response_model=List[CommentResponse])
def get_comments_by_assignment(assignment_id: UUID, db: Session = Depends(get_db)):
    try:
        comments = comments_crud.get_comments_by_assignment_id(db, assignment_id)
        return comments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@comments_router.get("/teachers/{teacher_id}/comments", status_code=status.HTTP_200_OK, response_model=List[CommentResponse])
def get_comments_by_teacher(teacher_id: UUID, db: Session = Depends(get_db)):
    try:
        comments = comments_crud.get_comments_by_teacher_id(db, teacher_id)
        return comments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@comments_router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment(comment_id: UUID, teacher_id: UUID, db: Session = Depends(get_db)):
    try:
        comments_crud.delete_comment(db, comment_id, teacher_id)
        db.commit()
        return {"detail": "Comment deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@comments_router.post("/{assignment_id}/likes", status_code=status.HTTP_201_CREATED, response_model=LikeCreate)
def add_like(assignment_id: UUID, like: LikeCreate, db: Session = Depends(get_db)):
    try:
        like = assignment_service.add_like(db, like, assignment_id)
        db.commit()
        return like
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

