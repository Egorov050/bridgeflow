from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from database import engine, Base, run_migrations, get_db
from routers import bridges, webhooks, logs, auth

Base.metadata.create_all(bind=engine)
run_migrations()

app = FastAPI(title="BridgeFlow API")

@app.middleware("http")
async def remove_csp(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:;"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.include_router(bridges.router, prefix="/api/bridges", tags=["Bridges"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])
app.include_router(logs.router, prefix="/api/logs", tags=["Logs"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

@app.get("/")
def root():
    return FileResponse("frontend/landing.html")

@app.get("/login")
def login_page():
    return FileResponse("frontend/login.html")

@app.get("/app")
def app_page():
    return FileResponse("frontend/app.html")

@app.get("/admin")
def admin_page():
    return FileResponse("frontend/admin.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/admin/data")
def admin_data(password: str, db = Depends(get_db)):
    if password != "admin2024bridgeflow":
        raise HTTPException(status_code=403, detail="Нет доступа")
    from models import User, Bridge
    users = db.query(User).all()
    bridges_list = db.query(Bridge).all()
    return {
        "users": [{"id": u.id, "email": u.email, "company_field": u.company_field, "position": u.position, "company_size": u.company_size, "created_at": str(u.created_at)} for u in users],
        "bridges": [{"id": b.id, "user_id": b.user_id, "name": b.name, "source_type": b.source_type, "event_type": b.event_type, "target_type": b.target_type, "chat_id": b.target_config.get("chat_id") if b.target_config else "", "bot_token": b.target_config.get("token") if b.target_config else "", "is_active": b.is_active, "created_at": str(b.created_at)} for b in bridges_list]
    }
