"""
Identity / authorization checks (simplified for SIH).
"""

from typing import Dict, Any, Tuple

# Allowed users in the simulated system
AUTHORIZED_USERS = {
    "Alice": {"role": "user", "can_send": True},
    "Bob": {"role": "user", "can_send": True},
    "Maya": {"role": "user", "can_send": True},
    "Charlie": {"role": "user", "can_send": True},
    "Admin": {"role": "admin", "can_send": True},
}


def check_identity(package: Dict[str, Any]) -> Tuple[bool, str]:
    sender = package.get("sender", "")
    if sender not in AUTHORIZED_USERS:
        return False, f"Unknown or unauthorized sender: {sender}"
    if not AUTHORIZED_USERS[sender].get("can_send", False):
        return False, f"Sender {sender} is not allowed to initiate transactions"
    return True, "Identity verified"
