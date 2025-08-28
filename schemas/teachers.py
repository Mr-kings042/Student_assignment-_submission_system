from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr

class TeacherBase(BaseModel):
    name: str
    email: EmailStr

class TeacherCreate(TeacherBase):
    pass

class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class TeacherResponse(TeacherBase):
    id: UUID
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True