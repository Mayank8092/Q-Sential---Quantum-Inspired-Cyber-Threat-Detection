"""
Attack Simulator for NightOwl SIH demo.
Generates legitimate packages then mutates them to simulate attacks.
"""

from typing import Dict, Any
from copy import deepcopy
from qds.protocol import create_qds_package
from database.db import is_nonce_used


def simulate_attack(attack_type: str, sender: str = "Alice", receiver: str = "Maya", amount: float = 1000.0) -> Dict[str, Any]:
    """
    Create a transaction package and optionally corrupt it according to attack_type.
    Returns the (possibly malicious) package + metadata about the attack.
    """
    # Always start from a clean legitimate package
    package = create_qds_package(sender=sender, receiver=receiver, amount=amount)

    attack_info = {
        "attack_type": attack_type,
        "description": "",
        "expected_decision": "ACCEPTED"
    }

    if attack_type == "normal":
        attack_info["description"] = "Legitimate transaction – no modification"
        attack_info["expected_decision"] = "ACCEPTED"

    elif attack_type == "forgery":
        # Change amount / receiver after signature was generated
        package["amount"] = amount * 10
        package["receiver"] = "Attacker"
        package["message"] = f"SEND {package['amount']} TO {package['receiver']}"
        # Keep original message_hash & qds_data → verification will fail
        attack_info["description"] = f"Forgery: amount changed to {package['amount']} and receiver to Attacker while QDS data stays original"
        attack_info["expected_decision"] = "REJECTED"

    elif attack_type == "replay":
        # Re-use the same nonce (we mark it used first)
        from database.db import mark_nonce_used
        mark_nonce_used(package["nonce"])
        attack_info["description"] = "Replay: same nonce is submitted again"
        attack_info["expected_decision"] = "REJECTED"

    elif attack_type == "impersonation":
        package["sender"] = "Eve"          # unauthorized identity
        attack_info["description"] = "Impersonation: sender set to unauthorized user 'Eve'"
        attack_info["expected_decision"] = "REJECTED"

    elif attack_type == "channel":
        # Corrupt measurement distribution (simulate quantum channel attack)
        md = package.get("measurement_data", {})
        counts = md.get("counts", {"00": 0, "01": 0, "10": 0, "11": 0})
        # Force a highly anomalous distribution
        shots = md.get("shots", 1024)
        package["measurement_data"]["counts"] = {
            "00": int(shots * 0.10),
            "01": int(shots * 0.40),
            "10": int(shots * 0.40),
            "11": int(shots * 0.10)
        }
        package["measurement_data"]["probabilities"] = {
            k: v / shots for k, v in package["measurement_data"]["counts"].items()
        }
        # Also mess up the expected initial state a bit
        if "qds_data" in package:
            package["qds_data"]["initial_state"] = "01"
        attack_info["description"] = "Channel manipulation: measurement statistics heavily distorted"
        attack_info["expected_decision"] = "REJECTED"

    else:
        attack_info["description"] = f"Unknown attack type: {attack_type}"
        attack_info["expected_decision"] = "REJECTED"

    return {
        "package": package,
        "attack_info": attack_info
    }
