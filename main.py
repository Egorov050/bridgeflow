from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine, Base
from routers import bridges, webhooks, logs, auth

from database import engine, Base, run_migrations

Base.metadata.create_all(bind=engine)
run_migrations()

app = FastAPI(title="BridgeFlow API")

from fastapi import Request
from fastapi.responses import Response

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


@app.get("/health")
def health():
    return {"status": "ok"}