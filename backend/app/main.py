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

#sign up if not yet registered
@app.post("/signup")
def signup(username: str, password: str, full_name: str, db: Session = Depends(get_db)):
    # check if username exists
    existing_user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if existing_user:
        return {"error": "Username already exists"}

    # create user
    new_user = models.User(
        username=username,
        password=password,
        role="student"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # create student profile
    new_student = models.Student(
        user_id=new_user.id,
        full_name=full_name,
        rank="6th kyu",  # default
        total_attendance=0
    )

    db.add(new_student)
    db.commit()

    return {"message": "User created successfully"}

#login
@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == username,
        models.User.password == password
    ).first()

    if not user:
        return {"error": "Invalid credentials"}

    student = db.query(models.Student).filter(
        models.Student.user_id == user.id
    ).first()

    return {
        "user_id": user.id,
        "role": user.role,
        "student_id": student.id if student else None
    }