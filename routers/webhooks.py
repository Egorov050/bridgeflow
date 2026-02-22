from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from models import Bridge, Log
from engine import process_event

router = APIRouter()

@router.post("/{event_type}")
async def receive_webhook(event_type: str, request: Request, db: Session = Depends(get_db)):
    # Получаем данные от Bitrix24
    form_data = await request.form()
    payload = dict(form_data)

    print(f"📥 Входящий вебхук: {event_type}, payload: {payload}")

    # Ищем активные мосты с этим событием
    bridges = db.query(Bridge).filter(
        Bridge.event_type == event_type.upper(),
        Bridge.is_active == True
    ).all()

    if not bridges:
        return {"ok": True, "message": "Нет активных мостов для этого события"}

    # Обрабатываем каждый мост
    for bridge in bridges:
        status, message = process_event(bridge, payload)

        # Пишем лог
        log = Log(
            bridge_id=bridge.id,
            status=status,
            payload=payload
        )
        db.add(log)

    db.commit()
    return {"ok": True, "processed": len(bridges)}