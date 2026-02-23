from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./bridgeflow.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_migrations():
    """Добавляем недостающие колонки если их нет"""
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE bridges ADD COLUMN user_id INTEGER"))
            conn.commit()
            print("Migration: added user_id to bridges")
        except Exception:
            pass  # Колонка уже есть