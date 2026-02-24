import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bridgeflow.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_migrations():
    with engine.connect() as conn:
        for column in [
            "ALTER TABLE bridges ADD COLUMN IF NOT EXISTS user_id INTEGER",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS company_field TEXT",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS position TEXT",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS company_size TEXT",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS onboarding_done BOOLEAN DEFAULT FALSE",
        ]:
            try:
                conn.execute(text(column))
                conn.commit()
            except Exception:
                pass
