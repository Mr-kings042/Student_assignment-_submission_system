from datetime import datetime
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel

class AssignmentBase(BaseModel):
    title: str
    subject: str
    description: str
    student_name: str


class AssignmentCreate(AssignmentBase):
    file_name: Optional[str] = None

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    student_name: Optional[str] = None
    description: Optional[str] = None
    file_name: Optional[str] = None


class CommentBase(BaseModel):
    content: str
   

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentResponse(CommentBase):
    id: UUID
    teacher_id: UUID
    assignment_id: UUID
    created_at: datetime
    class Config:
        from_attributes = True
    

class LikeBase(BaseModel):
    teacher_id: UUID
    assignment_id: UUID

class LikeCreate(LikeBase):
    pass

class LikeResponse(LikeBase):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True


class AssignmentResponse(AssignmentBase):
    id: UUID
    student_id: UUID
    is_submitted: bool = False
    file_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    comments: list[CommentResponse] = []
    likes: list[LikeResponse] = []
    class Config:
        from_attributes = True