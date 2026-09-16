"""
QDS Verification API – the heart of NightOwl.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

from security.validation import validate_package
from security.identity import check_identity
from security.replay import check_replay
from security.timestamp import check_timestamp
from qds.protocol import verify_qds_package
from database.db import save_verification, mark_nonce_used

router = APIRouter()


class VerifyRequest(BaseModel):
    package: Dict[str, Any]


@router.post("/verify")
async def verify_qds(req: VerifyRequest):
    """
    Full NightOwl verification pipeline:
    1. Input validation
    2. Identity check
    3. Timestamp check
    4. Nonce / replay check
    5. Quantum verification (Qiskit)
    6. Statistical analysis
    7. Decision
    """
    package = req.package
    steps = []
    threats = []

    # ---- Step 1: Input validation ----
    ok, msg = validate_package(package)
    steps.append({"step": "Input Validation", "status": "PASS" if ok else "FAIL", "detail": msg})
    if not ok:
        result = _build_result(package, "REJECTED", steps, threats + ["INVALID_INPUT"], msg)
        save_verification(result)
        return result

    # ---- Step 2: Identity ----
    ok, msg = check_identity(package)
    steps.append({"step": "Identity Check", "status": "PASS" if ok else "FAIL", "detail": msg})
    if not ok:
        threats.append("IMPERSONATION")
        result = _build_result(package, "REJECTED", steps, threats, msg)
        save_verification(result)
        return result

    # ---- Step 3: Timestamp ----
    ok, msg = check_timestamp(package)
    steps.append({"step": "Timestamp Check", "status": "PASS" if ok else "FAIL", "detail": msg})
    if not ok:
        threats.append("STALE_REQUEST")
        result = _build_result(package, "REJECTED", steps, threats, msg)
        save_verification(result)
        return result

    # ---- Step 4: Nonce / Replay ----
    ok, msg = check_replay(package)
    steps.append({"step": "Nonce / Replay Check", "status": "PASS" if ok else "FAIL", "detail": msg})
    if not ok:
        threats.append("REPLAY_ATTACK")
        result = _build_result(package, "REJECTED", steps, threats, msg)
        save_verification(result)
        return result

    # ---- Step 5: Quantum verification ----
    try:
        q_result = verify_qds_package(package)
        steps.append({
            "step": "QDS Protocol / Bell / Teleportation / Pauli",
            "status": "PASS" if q_result["valid_qds"] else "FAIL",
            "detail": f"Quantum decision: {q_result['decision_quantum']}"
        })
        steps.append({
            "step": "Measurement + Statistical Analysis",
            "status": "PASS" if q_result["decision_quantum"] == "ACCEPTED" else "WARN" if q_result["decision_quantum"] == "FLAGGED" else "FAIL",
            "detail": f"TVD={q_result['statistics']['total_variation_distance']:.4f}, p={q_result['statistics']['p_value']:.4f}"
        })
    except Exception as e:
        steps.append({"step": "Quantum Engine", "status": "FAIL", "detail": str(e)})
        result = _build_result(package, "REJECTED", steps, threats + ["QUANTUM_ENGINE_ERROR"], str(e))
        save_verification(result)
        return result

    # ---- Final decision ----
    decision = q_result["decision_quantum"]
    if decision == "REJECTED":
        threats.append("QUANTUM_VERIFICATION_FAILED")
        # Could also be forgery or channel anomaly
        if package.get("amount") and "Attacker" in str(package.get("receiver", "")):
            threats.append("FORGERY_SUSPECTED")
        else:
            threats.append("CHANNEL_ANOMALY")

    # Mark nonce only on successful accept (or always after processing to prevent replay)
    mark_nonce_used(package["nonce"])

    result = _build_result(
        package,
        decision,
        steps,
        threats,
        f"NightOwl decision: {decision}",
        quantum=q_result
    )
    save_verification(result)
    return result


def _build_result(package, decision, steps, threats, message, quantum=None):
    return {
        "transaction_id": package.get("transaction_id"),
        "sender": package.get("sender"),
        "receiver": package.get("receiver"),
        "amount": package.get("amount"),
        "nonce": package.get("nonce"),
        "timestamp": package.get("timestamp"),
        "decision": decision,
        "threats": threats,
        "steps": steps,
        "message": message,
        "quantum": quantum,
        "verified_at": datetime.utcnow().isoformat() + "Z",
        "package": package
    }
