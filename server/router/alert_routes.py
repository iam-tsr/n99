from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from config.pg_config import get_db
from model.db.models import MovieAlert, User
from router.auth_routes import get_current_user

router = APIRouter(prefix="/alerts", tags=["alerts"])

class AlertCreate(BaseModel):
    movie_name: str
    cinema_place: str
    target_date: str # YYYY-MM-DD

class AlertResponse(BaseModel):
    id: int
    movie_name: str
    cinema_place: str
    target_date: str
    is_fulfilled: bool
    
    class Config:
        orm_mode = True

@router.post("/", response_model=AlertResponse)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_alert = MovieAlert(
        user_id=current_user.id,
        movie_name=alert.movie_name,
        cinema_place=alert.cinema_place,
        target_date=alert.target_date
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return new_alert

@router.get("/", response_model=List[AlertResponse])
def get_user_alerts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alerts = db.query(MovieAlert).filter(MovieAlert.user_id == current_user.id).all()
    return alerts
