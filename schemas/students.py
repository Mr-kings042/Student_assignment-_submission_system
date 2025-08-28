from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel,EmailStr



class StudentBase(BaseModel):
    name: str
    email: EmailStr
  

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
class StudentResponse(StudentBase):
    id: UUID
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        form_attributes = True