"""
Dashboard / history / threats API.
"""

from fastapi import APIRouter
from database.db import get_stats, get_history, get_threats

router = APIRouter()


@router.get("/stats")
async def stats():
    return get_stats()


@router.get("/history")
async def history(limit: int = 20):
    return get_history(limit=limit)


@router.get("/threats")
async def threats(limit: int = 20):
    return get_threats(limit=limit)
