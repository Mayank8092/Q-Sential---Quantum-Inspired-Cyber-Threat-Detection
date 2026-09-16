"""
Simple in-memory + JSON file persistence for SIH prototype.
No external DB required.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import threading

DB_FILE = os.path.join(os.path.dirname(__file__), "nightowl_data.json")
_lock = threading.Lock()

_default = {
    "transactions": [],
    "verifications": [],
    "threats": [],
    "nonces": [],
    "counter": 0
}


def _load() -> dict:
    if not os.path.exists(DB_FILE):
        return _default.copy()
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return _default.copy()


def _save(data: dict):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def init_db():
    data = _load()
    if "transactions" not in data:
        data = _default.copy()
        _save(data)
    print(f"📦 Database ready → {DB_FILE}")


def next_txn_id() -> str:
    with _lock:
        data = _load()
        data["counter"] = data.get("counter", 0) + 1
        _save(data)
        return f"NW-TXN-{datetime.utcnow().strftime('%Y%m%d')}-{data['counter']:04d}"


def save_transaction(txn: dict):
    with _lock:
        data = _load()
        data["transactions"].append(txn)
        _save(data)


def save_verification(result: dict):
    with _lock:
        data = _load()
        data["verifications"].append(result)
        if result.get("decision") in ("REJECTED", "FLAGGED"):
            data["threats"].append(result)
        # Store nonce
        nonce = result.get("nonce") or (result.get("package") or {}).get("nonce")
        if nonce and nonce not in data["nonces"]:
            data["nonces"].append(nonce)
        _save(data)


def is_nonce_used(nonce: str) -> bool:
    data = _load()
    return nonce in data.get("nonces", [])


def mark_nonce_used(nonce: str):
    with _lock:
        data = _load()
        if nonce not in data["nonces"]:
            data["nonces"].append(nonce)
            _save(data)


def get_stats() -> dict:
    data = _load()
    verifs = data.get("verifications", [])
    accepted = sum(1 for v in verifs if v.get("decision") == "ACCEPTED")
    rejected = sum(1 for v in verifs if v.get("decision") == "REJECTED")
    flagged = sum(1 for v in verifs if v.get("decision") == "FLAGGED")
    threats = len(data.get("threats", []))
    return {
        "total": len(verifs),
        "accepted": accepted,
        "rejected": rejected,
        "flagged": flagged,
        "threats": threats,
        "transactions": len(data.get("transactions", []))
    }


def get_history(limit: int = 20) -> List[dict]:
    data = _load()
    verifs = data.get("verifications", [])
    return list(reversed(verifs[-limit:]))


def get_threats(limit: int = 20) -> List[dict]:
    data = _load()
    threats = data.get("threats", [])
    return list(reversed(threats[-limit:]))


def get_transaction(txn_id: str) -> Optional[dict]:
    data = _load()
    for t in data.get("transactions", []):
        if t.get("transaction_id") == txn_id:
            return t
    return None
