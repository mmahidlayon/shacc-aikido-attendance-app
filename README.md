# SHACC Aikido Attendance App (Backend)

A system for tracking student attendance in our Aikido dojo (SHACC).
This helps students monitor their progress toward rank promotion.

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL

---

## Features

### Student
- Record attendance
- View total sessions attended
- Track progress toward next rank

### Admin (Sensei / Senpai)
- View all students
- Monitor attendance records
- Verify attendance

---

## Rank Requirements

| From Rank | To Rank | Required Sessions |
|-----------|---------|-------------------|
| 6th kyu   | 5th kyu | 45                |
| 5th kyu   | 4th kyu | 60                |
| 4th kyu   | 3rd kyu | 75                |
| 3rd kyu   | 2nd kyu | 75                |
| 2nd kyu   | 1st kyu | 90                |

---

## Project Setup

### 1. Clone Repository
```bash
git clone https://github.com/mmahidlayon/shacc-attendance-app-backend.git
cd shacc-attendance-app-backend
