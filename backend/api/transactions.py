"""
Transaction generation API.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from qds.protocol import create_qds_package
from database.db import save_transaction

router = APIRouter()


class TransactionRequest(BaseModel):
    sender: str = Field(..., example="Alice")
    receiver: str = Field(..., example="Maya")
    amount: float = Field(..., gt=0, example=1000.0)


@router.post("/transactions")
@router.post("/generate-signature")
async def generate_transaction(req: TransactionRequest):
    """
    Generate a complete simulated QDS transaction package.
    User only supplies sender, receiver, amount.
    Everything else (ID, nonce, hash, quantum data) is automatic.
    """
    try:
        package = create_qds_package(
            sender=req.sender.strip(),
            receiver=req.receiver.strip(),
            amount=float(req.amount)
        )
        save_transaction(package)
        return {
            "status": "success",
            "message": "Transaction + QDS package generated",
            "package": package
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
