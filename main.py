from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import bridges, webhooks, logs

Base.metadata.create_all(bind=engine)

app = FastAPI(title="BridgeFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bridges.router,  prefix="/api/bridges",  tags=["Bridges"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["Webhooks"])
app.include_router(logs.router,     prefix="/api/logs",     tags=["Logs"])

@app.get("/")
def root():
    return {"status": "ok", "service": "BridgeFlow"}