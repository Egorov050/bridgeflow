from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Bridge(Base):
    __tablename__ = "bridges"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String, nullable=False)
    is_active     = Column(Boolean, default=True)

    source_type   = Column(String)   # "bitrix24"
    source_config = Column(JSON)     # {"domain": "...", "token": "..."}
    event_type    = Column(String)   # "ONCRMDEALADD"

    target_type   = Column(String)   # "myteam"
    target_config = Column(JSON)     # {"token": "...", "chat_id": "..."}

    template      = Column(Text)     # "🔔 Новая сделка!\nНазвание: {TITLE}"

    created_at    = Column(DateTime, server_default=func.now())


class Log(Base):
    __tablename__ = "logs"

    id           = Column(Integer, primary_key=True, index=True)
    bridge_id    = Column(Integer, ForeignKey("bridges.id"))
    status       = Column(String)   # "success" / "error"
    payload      = Column(JSON)
    triggered_at = Column(DateTime, server_default=func.now())