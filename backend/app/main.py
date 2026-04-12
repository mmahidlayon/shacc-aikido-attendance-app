from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date

from .database import engine, SessionLocal
from . import models

app = FastAPI()

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)


# ✅ CORS (VERY IMPORTANT for frontend)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Dependency: DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Root (already working)
@app.get("/")
def root():
    return {"message": "SHACC Backend is running!"}


# ✅ Record Attendance
@app.post("/attendance")
def record_attendance(student_id: int, notes: str = "", db: Session = Depends(get_db)):
    new_attendance = models.Attendance(
        student_id=student_id,
        session_date=date.today(),
        notes=notes
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return {"message": "Attendance recorded successfully"}


# ✅ Get Attendance by Student
@app.get("/attendance/{student_id}")
def get_attendance(student_id: int, db: Session = Depends(get_db)):
    records = db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id
    ).all()

    return records