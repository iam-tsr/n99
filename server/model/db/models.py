from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config.pg_config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to movie alerts
    alerts = relationship("MovieAlert", back_populates="user", cascade="all, delete-orphan")

class MovieAlert(Base):
    __tablename__ = "movie_alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_name = Column(String, index=True, nullable=False)
    cinema_place = Column(String, nullable=False)
    target_date = Column(String, nullable=False) # store as YYYY-MM-DD
    is_fulfilled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship back to the user
    user = relationship("User", back_populates="alerts")
