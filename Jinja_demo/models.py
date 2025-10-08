from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./students.db"  # same DB file

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# -------------------
# Existing Students Table
# -------------------
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(String)

# -------------------
# New Cafe Booking Table
# -------------------
class CafeBooking(Base):
    __tablename__ = "cafe_bookings"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)           # booking date
    time_slot = Column(String, nullable=False)    # time slot string
    name = Column(String, nullable=False)         # customer name
    phone = Column(String, nullable=False)        # phone number

# Create tables
Base.metadata.create_all(bind=engine)
