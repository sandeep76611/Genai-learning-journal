from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date, datetime

from models import SessionLocal, Student, CafeBooking

app = FastAPI()

# --- Static & templates ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# --- DB Session Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Home Page ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    topics = [
        {"title": "Jinja2 Basics", "description": "Learn template inheritance and variables", "link": "/jinja-basics"},
        {"title": "CRUD Practice", "description": "Perform CRUD with FastAPI & Jinja2", "link": "/students"},
        {"title": "Café Booking", "description": "Book tables in real time", "link": "/cafe-booking"},
    ]
    return templates.TemplateResponse("index.html", {"request": request, "topics": topics})


# ==============================
#  STUDENTS CRUD
# ==============================

@app.get("/students", response_class=HTMLResponse)
def list_students(request: Request):
    db = SessionLocal()
    students = db.query(Student).all()
    db.close()
    return templates.TemplateResponse("crud.html", {"request": request, "students": students, "title": "Students"})


@app.get("/students/new", response_class=HTMLResponse)
def new_student_form(request: Request):
    return templates.TemplateResponse("student_form.html", {"request": request, "title": "Add Student"})


@app.post("/students/new")
def create_student(name: str = Form(...), age: int = Form(...), grade: str = Form(...)):
    db = SessionLocal()
    new_stud = Student(name=name, age=age, grade=grade)
    db.add(new_stud)
    db.commit()
    db.close()
    return RedirectResponse(url="/students", status_code=303)


@app.get("/students/edit/{student_id}", response_class=HTMLResponse)
def edit_student_form(request: Request, student_id: int):
    db = SessionLocal()
    student = db.query(Student).get(student_id)
    db.close()
    return templates.TemplateResponse("student_form.html", {"request": request, "student": student, "title": "Edit Student"})


@app.post("/students/edit/{student_id}")
def update_student(student_id: int, name: str = Form(...), age: int = Form(...), grade: str = Form(...)):
    db = SessionLocal()
    student = db.query(Student).get(student_id)
    student.name = name
    student.age = age
    student.grade = grade
    db.commit()
    db.close()
    return RedirectResponse(url="/students", status_code=303)


@app.get("/students/delete/{student_id}")
def delete_student(student_id: int):
    db = SessionLocal()
    student = db.query(Student).get(student_id)
    db.delete(student)
    db.commit()
    db.close()
    return RedirectResponse(url="/students", status_code=303)


# ==============================
#  CAFE BOOKING CRUD
# ==============================

@app.get("/cafe-booking", response_class=HTMLResponse)
def cafe_booking(request: Request):
    """Show bookings and booking form."""
    db = SessionLocal()
    bookings = db.query(CafeBooking).order_by(CafeBooking.date.asc(),CafeBooking.time_slot.asc()).all()
    db.close()
    today = date.today().isoformat()  # min date for input field
    return templates.TemplateResponse(
        "cafe_booking.html",
        {"request": request, "bookings": bookings, "today": today, "title": "Café Booking"}
    )


@app.post("/cafe-booking")
def create_booking(date: str = Form(...), time_slot: str = Form(...), name: str = Form(...), phone: str = Form(...)):
    """Create a new booking if table available."""
    db: Session = SessionLocal()
    booking_date = datetime.strptime(date, "%Y-%m-%d").date()

    # Check if the same time slot already booked
    existing = db.query(CafeBooking).filter(
        CafeBooking.date == booking_date,
        CafeBooking.time_slot == time_slot
    ).first()

    if existing:
        db.close()
        # redirect back with error message in production
        return RedirectResponse(url="/cafe-booking", status_code=303)

    new_booking = CafeBooking(
        date=booking_date,
        time_slot=time_slot,
        name=name,
        phone=phone
    )
    db.add(new_booking)
    db.commit()
    db.close()
    return RedirectResponse(url="/cafe-booking", status_code=303)


@app.get("/cafe-booking/delete/{booking_id}")
def delete_booking(booking_id: int):
    """Delete (cancel) a booking."""
    db = SessionLocal()
    booking = db.query(CafeBooking).get(booking_id)
    db.delete(booking)
    db.commit()
    db.close()
    return RedirectResponse(url="/cafe-booking", status_code=303)
