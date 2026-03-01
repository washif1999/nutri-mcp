import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from ..core.database import Base

class AuthKey(Base):
    """API keys for authentication."""
    __tablename__ = "authkeys"
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, unique=True, index=True, nullable=False)
    client_name = Column(String, nullable=False)

class Meal(Base):
    """Stores logged meals with macro information."""
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    protein = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    calories = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Complaint(Base):
    """Stores logged health complaints with severity ratings."""
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    severity = Column(Integer, nullable=False)  # 1-10
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Hospital(Base):
    """Best hospitals for doctor appointments."""
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    rating = Column(Float, nullable=False)  # 0.0 - 5.0
    contact = Column(String)
    address = Column(String)

class Appointment(Base):
    """Doctor appointments auto-booked for severe complaints."""
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    status = Column(String, default="scheduled")  # scheduled / cancelled / completed
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
