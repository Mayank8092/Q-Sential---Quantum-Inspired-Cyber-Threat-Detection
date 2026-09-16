"""
NightOwl - Quantum Digital Signature (QDS) Verification + Cyber-Threat Detection System
SIH Prototype - Simulated Transaction + Teleportation-based QDS Environment
"""

from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
from datetime import datetime
from typing import Optional

from api.transactions import router as transactions_router
from api.verification import router as verification_router
from api.attacks import router as attacks_router
from api.dashboard import router as dashboard_router
from database.db import init_db, get_stats, get_history, get_threats

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

app = FastAPI(
    title="NightOwl",
    description="Quantum-Inspired QDS Security & Cyber-Threat Detection System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static & Templates
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Include API routers
app.include_router(transactions_router, prefix="/api", tags=["Transactions"])
app.include_router(verification_router, prefix="/api", tags=["Verification"])
app.include_router(attacks_router, prefix="/api", tags=["Attacks"])
app.include_router(dashboard_router, prefix="/api", tags=["Dashboard"])


@app.on_event("startup")
async def startup():
    init_db()
    print("🦉 NightOwl started successfully")
    print("   Dashboard  → http://127.0.0.1:8000/")
    print("   API Docs   → http://127.0.0.1:8000/api/docs")


# ==================== FRONTEND ROUTES ====================

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    stats = get_stats()
    history = get_history(limit=5)
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"stats": stats, "history": history, "page": "dashboard"}
    )


@app.get("/generate", response_class=HTMLResponse)
async def generate_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="generate.html",
        context={"page": "generate"}
    )


@app.get("/verify", response_class=HTMLResponse)
async def verify_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="verify.html",
        context={"page": "verify"}
    )


@app.get("/attacks", response_class=HTMLResponse)
async def attacks_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="attacks.html",
        context={"page": "attacks"}
    )


@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    history = get_history(limit=50)
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={"history": history, "page": "history"}
    )


@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    threats = get_threats(limit=30)
    stats = get_stats()
    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={"threats": threats, "stats": stats, "page": "reports"}
    )


@app.get("/health")
async def health():
    return {"status": "ok", "service": "NightOwl", "time": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)