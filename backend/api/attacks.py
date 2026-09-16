"""
Attack Simulator API.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from attacks.simulator import simulate_attack
from api.verification import verify_qds, VerifyRequest

router = APIRouter()


class AttackRequest(BaseModel):
    attack_type: str = Field(..., example="forgery", description="normal | forgery | replay | impersonation | channel")
    sender: str = "Alice"
    receiver: str = "Maya"
    amount: float = 1000.0


@router.post("/simulate-attack")
async def run_attack(req: AttackRequest):
    """
    Generate a (possibly malicious) package and immediately run it through NightOwl verification.
    Perfect for live SIH demo.
    """
    valid_types = {"normal", "forgery", "replay", "impersonation", "channel"}
    if req.attack_type not in valid_types:
        raise HTTPException(400, f"attack_type must be one of {valid_types}")

    sim = simulate_attack(
        attack_type=req.attack_type,
        sender=req.sender,
        receiver=req.receiver,
        amount=req.amount
    )

    # Run through the real verification pipeline
    verify_req = VerifyRequest(package=sim["package"])
    result = await verify_qds(verify_req)

    return {
        "attack_info": sim["attack_info"],
        "package": sim["package"],
        "verification": result
    }
