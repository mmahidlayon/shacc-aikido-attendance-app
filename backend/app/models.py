# backend/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    student = relationship("Student", back_populates="user", uselist=False)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    full_name = Column(String, nullable=False)
    rank = Column(String, default="6th kyu")
    total_attendance = Column(Integer, default=0)

    user = relationship("User", back_populates="student")
    attendance_records = relationship("Attendance", back_populates="student")

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    session_date = Column(Date, nullable=False)
    notes = Column(Text)

    student = relationship("Student", back_populates="attendance_records")

class Rank(Base):
    __tablename__ = "ranks"
    id = Column(Integer, primary_key=True, index=True)
    rank_name = Column(String, unique=True, nullable=False)
    attendance_required = Column(Integer, nullable=False)
