"""
Nonce / Replay-attack detection.
"""

from typing import Dict, Any, Tuple
from database.db import is_nonce_used, mark_nonce_used


def check_replay(package: Dict[str, Any]) -> Tuple[bool, str]:
    nonce = package.get("nonce")
    if not nonce:
        return False, "Missing nonce"

    if is_nonce_used(nonce):
        return False, "REPLAY ATTACK: Nonce already used"

    # Mark as used only after successful full verification
    # (caller will call mark_nonce_used on success)
    return True, "Nonce is fresh"
