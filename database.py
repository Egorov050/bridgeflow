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
    with engine.connect() as conn:
        for column in [
            "ALTER TABLE bridges ADD COLUMN user_id INTEGER",
            "ALTER TABLE users ADD COLUMN company_field TEXT",
            "ALTER TABLE users ADD COLUMN position TEXT",
            "ALTER TABLE users ADD COLUMN company_size TEXT",
            "ALTER TABLE users ADD COLUMN onboarding_done INTEGER DEFAULT 0",
        ]:
            try:
                conn.execute(text(column))
                conn.commit()
            except Exception:
                pass