from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from models import Bridge, Log
from engine import process_event

router = APIRouter()

@router.post("/{event_type}/{user_id}")
async def receive_webhook_user(event_type: str, user_id: int, request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    payload = dict(form_data)
    print(f"📥 Вебхук: {event_type} user_id={user_id}, payload: {payload}")

    bridges = db.query(Bridge).filter(
        Bridge.event_type == event_type.upper(),
        Bridge.user_id == user_id,
        Bridge.is_active == True
    ).all()

    if not bridges:
        return {"ok": True, "message": "Нет активных мостов"}

    for bridge in bridges:
        status, message = process_event(bridge, payload)
        log = Log(bridge_id=bridge.id, status=status, payload=payload)
        db.add(log)

    db.commit()
    return {"ok": True, "processed": len(bridges)}

@router.post("/{event_type}")
async def receive_webhook(event_type: str, request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    payload = dict(form_data)
    print(f"📥 Вебхук: {event_type}, payload: {payload}")

    bridges = db.query(Bridge).filter(
        Bridge.event_type == event_type.upper(),
        Bridge.is_active == True
    ).all()

    if not bridges:
        return {"ok": True, "message": "Нет активных мостов"}

    for bridge in bridges:
        status, message = process_event(bridge, payload)
        log = Log(bridge_id=bridge.id, status=status, payload=payload)
        db.add(log)

    db.commit()
    return {"ok": True, "processed": len(bridges)}
