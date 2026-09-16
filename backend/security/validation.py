"""
Input validation for NightOwl.
"""

from typing import Dict, Any, Tuple


def validate_package(package: Dict[str, Any]) -> Tuple[bool, str]:
    required = [
        "transaction_id", "sender", "receiver", "amount",
        "timestamp", "nonce", "message", "message_hash",
        "protocol", "qds_data", "measurement_data"
    ]
    for key in required:
        if key not in package or package[key] is None:
            return False, f"Missing required field: {key}"

    if not isinstance(package["amount"], (int, float)) or package["amount"] <= 0:
        return False, "Invalid amount"

    if not package["sender"] or not package["receiver"]:
        return False, "Sender/Receiver cannot be empty"

    if package.get("protocol") != "Teleportation-QDS-v1":
        return False, f"Unsupported protocol: {package.get('protocol')}"

    if not package.get("qds_data"):
        return False, "Missing qds_data"

    if not package.get("measurement_data"):
        return False, "Missing measurement_data"

    return True, "OK"
