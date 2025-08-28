import uuid
from datetime import datetime
from sqlalchemy import Column,  String, Boolean,Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.database import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    subject = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    file_name = Column(Text, nullable=True)
    student_name= Column(String, nullable=False)
    student_id = Column(UUID(as_uuid=True),ForeignKey("students.id"), nullable=False)
    is_submitted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="assignments")
    comments = relationship("Comment", back_populates="assignment", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="assignment", cascade="all, delete-orphan")


class Comment(Base):
       __tablename__ = "comments"

       id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
       teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), nullable=False)
       assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignments.id"), nullable=False)
       content = Column(Text, nullable=False)
       created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
       teacher = relationship("Teacher", back_populates="comments")
       assignment = relationship("Assignment", back_populates="comments")


class Like(Base):
       __tablename__ = "likes"

       id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
       teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), nullable=False)
       assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignments.id"), nullable=False)
       created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

       teacher = relationship("Teacher", back_populates="likes")
       assignment = relationship("Assignment", back_populates="likes")
