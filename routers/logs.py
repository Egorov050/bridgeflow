from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Log, Bridge

router = APIRouter()

@router.get("/")
def get_all_logs(user_id: int = 0, db: Session = Depends(get_db)):
    if user_id:
        bridge_ids = [b.id for b in db.query(Bridge).filter(Bridge.user_id == user_id).all()]
        return db.query(Log).filter(Log.bridge_id.in_(bridge_ids)).order_by(Log.triggered_at.desc()).limit(50).all()
    return db.query(Log).order_by(Log.triggered_at.desc()).limit(50).all()

@router.get("/{bridge_id}")
def get_logs_by_bridge(bridge_id: int, db: Session = Depends(get_db)):
    return db.query(Log).filter(Log.bridge_id == bridge_id).order_by(Log.triggered_at.desc()).all()