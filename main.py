from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import bridges, webhooks, logs



Base.metadata.create_all(bind=engine)

app = FastAPI(title="BridgeFlow API")

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers import bridges, webhooks, logs, auth

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/ui")
def ui():
    return FileResponse("frontend/index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    email         = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at    = Column(DateTime, server_default=func.now())

app.include_router(bridges.router,  prefix="/api/bridges",  tags=["Bridges"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])
app.include_router(logs.router,     prefix="/api/logs",     tags=["Logs"])

@app.get("/")
def root():
    return {"status": "ok", "service": "BridgeFlow"}

@app.get("/login")
def login_page():
    return FileResponse("frontend/login.html")

@app.get("/app")
def app_page():
    return FileResponse("frontend/index.html")