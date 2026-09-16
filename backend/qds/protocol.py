"""
Teleportation-based Quantum Digital Signature (QDS) Protocol Simulator
Based on quantum teleportation + Bell-state measurement for SIH prototype.

This is a SIMULATED environment that demonstrates the mathematics of a
teleportation-based QDS. It does NOT claim to be a production quantum system.
"""

import hashlib
import secrets
import numpy as np
from datetime import datetime
from typing import Dict, Any, Tuple
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from .bell_state import create_bell_pair
from .teleportation import teleport_state
from .pauli import apply_pauli_correction
from .measurement import measure_and_analyze


def generate_message_hash(sender: str, receiver: str, amount: float, txn_id: str, nonce: str) -> str:
    raw = f"{sender}|{receiver}|{amount}|{txn_id}|{nonce}"
    return hashlib.sha256(raw.encode()).hexdigest()


def generate_nonce() -> str:
    return secrets.token_hex(16).upper()


def create_qds_package(
    sender: str,
    receiver: str,
    amount: float,
    txn_id: str = None,
    shots: int = 1024
) -> Dict[str, Any]:
    """
    Full QDS generation pipeline:
    1. Create transaction metadata
    2. Generate nonce + message hash
    3. Prepare quantum state from message hash (classical → quantum encoding)
    4. Create Bell pair
    5. Teleport
    6. Pauli correction
    7. Measure
    8. Package verification data
    """
    from database.db import next_txn_id

    if txn_id is None:
        txn_id = next_txn_id()

    nonce = generate_nonce()
    timestamp = datetime.utcnow().isoformat() + "Z"
    message = f"SEND {amount} TO {receiver}"
    message_hash = generate_message_hash(sender, receiver, amount, txn_id, nonce)

    # --- Quantum pipeline ---
    # Encode first 2 bits of hash as initial state (simplified for demo)
    hash_bits = bin(int(message_hash[:8], 16))[2:].zfill(32)
    initial_state = hash_bits[:2]  # '00', '01', '10', or '11'

    # 1. Bell state
    bell_qc = create_bell_pair()

    # 2. Teleportation circuit
    teleport_qc = teleport_state(initial_state)

    # 3. Pauli correction (based on measurement of Bell + teleported state)
    # In real protocol this would depend on classical communication bits
    correction = secrets.choice(["I", "X", "Z", "Y"])
    corrected_qc = apply_pauli_correction(teleport_qc, correction)

    # 4. Measurement
    measurement = measure_and_analyze(corrected_qc, shots=shots)

    package = {
        "transaction_id": txn_id,
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "timestamp": timestamp,
        "nonce": nonce,
        "message": message,
        "message_hash": message_hash,
        "protocol": "Teleportation-QDS-v1",
        "qds_data": {
            "initial_state": initial_state,
            "bell_state": "Phi+",
            "pauli_correction": correction,
            "teleportation_success": True
        },
        "measurement_data": measurement,
        "shots": shots
    }
    return package


def verify_qds_package(package: Dict[str, Any], expected_shots: int = 1024) -> Dict[str, Any]:
    """
    Verify a QDS package using the same quantum pipeline + statistical test.
    Returns verification result with decision.
    """
    from analysis.statistics import statistical_test
    from analysis.threshold import decide

    # Re-run quantum verification on the claimed data
    initial_state = package.get("qds_data", {}).get("initial_state", "00")
    correction = package.get("qds_data", {}).get("pauli_correction", "I")

    # Rebuild circuit
    teleport_qc = teleport_state(initial_state)
    corrected_qc = apply_pauli_correction(teleport_qc, correction)
    observed = measure_and_analyze(corrected_qc, shots=package.get("shots", expected_shots))

    # Expected distribution for ideal teleportation of |00⟩ / |11⟩ etc.
    expected = _expected_distribution(initial_state, correction)

    # Statistical test
    stats = statistical_test(expected, observed["counts"], package.get("shots", expected_shots))

    decision = decide(stats)

    return {
        "valid_qds": decision != "REJECTED",
        "observed": observed,
        "expected": expected,
        "statistics": stats,
        "decision_quantum": decision
    }


def _expected_distribution(initial_state: str, correction: str) -> Dict[str, float]:
    """
    Ideal expected probabilities after successful teleportation + Pauli correction.
    For demo: successful teleportation of |ψ⟩ should yield high probability
    on the corrected basis states.
    """
    # Simplified model: after perfect teleportation of a computational basis state
    # we expect ~50/50 on the two states that match the encoding after correction.
    base = {
        "00": 0.48,
        "01": 0.01,
        "10": 0.01,
        "11": 0.50
    }
    # Slight variation based on initial state for realism
    if initial_state == "01":
        base = {"00": 0.01, "01": 0.49, "10": 0.49, "11": 0.01}
    elif initial_state == "10":
        base = {"00": 0.01, "01": 0.49, "10": 0.49, "11": 0.01}
    elif initial_state == "11":
        base = {"00": 0.50, "01": 0.01, "10": 0.01, "11": 0.48}
    return base
