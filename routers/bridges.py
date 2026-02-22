from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Bridge

router = APIRouter()

class BridgeCreate(BaseModel):
    name: str
    source_type: str
    source_config: dict
    event_type: str
    target_type: str
    target_config: dict
    template: str

class BridgeUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    template: Optional[str] = None

@router.get("/")
def get_bridges(db: Session = Depends(get_db)):
    return db.query(Bridge).all()

@router.post("/")
def create_bridge(data: BridgeCreate, db: Session = Depends(get_db)):
    bridge = Bridge(**data.model_dump())
    db.add(bridge)
    db.commit()
    db.refresh(bridge)
    return bridge

@router.get("/{bridge_id}")
def get_bridge(bridge_id: int, db: Session = Depends(get_db)):
    bridge = db.query(Bridge).filter(Bridge.id == bridge_id).first()
    if not bridge:
        raise HTTPException(status_code=404, detail="Мост не найден")
    return bridge

@router.patch("/{bridge_id}")
def update_bridge(bridge_id: int, data: BridgeUpdate, db: Session = Depends(get_db)):
    bridge = db.query(Bridge).filter(Bridge.id == bridge_id).first()
    if not bridge:
        raise HTTPException(status_code=404, detail="Мост не найден")
    for key, value in data.model_dump(exclude_none=True).items():
        setattr(bridge, key, value)
    db.commit()
    db.refresh(bridge)
    return bridge

@router.delete("/{bridge_id}")
def delete_bridge(bridge_id: int, db: Session = Depends(get_db)):
    bridge = db.query(Bridge).filter(Bridge.id == bridge_id).first()
    if not bridge:
        raise HTTPException(status_code=404, detail="Мост не найден")
    db.delete(bridge)
    db.commit()
    return {"ok": True}

from models import Log

@router.get("/{bridge_id}/logs")
def get_bridge_logs(bridge_id: int, db: Session = Depends(get_db)):
    logs = db.query(Log).filter(Log.bridge_id == bridge_id).order_by(Log.triggered_at.desc()).all()
    return logs
