import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(String, default=datetime.utcnow)
    updated_at = Column(String, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    comments = relationship("Comment", back_populates="teacher")
    likes = relationship("Like", back_populates="teacher")
