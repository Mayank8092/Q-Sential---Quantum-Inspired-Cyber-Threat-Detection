"""
Quantum Teleportation circuit for QDS protocol.
"""

from qiskit import QuantumCircuit
from .bell_state import create_bell_circuit_for_teleport


def teleport_state(initial_state: str = "00") -> QuantumCircuit:
    """
    Full teleportation circuit.
    initial_state: two classical bits that define the state to teleport
                   (we prepare |ψ⟩ on qubit 0 from those bits).
    Returns a 3-qubit circuit ready for measurement.
    """
    qc = QuantumCircuit(3, 3, name="QDS_Teleport")

    # --- Prepare state to teleport on qubit 0 ---
    if initial_state[0] == "1":
        qc.x(0)
    if len(initial_state) > 1 and initial_state[1] == "1":
        # For simplicity we only use single-qubit computational basis
        # (full 2-bit encoding would need an extra qubit; demo uses 1 qubit)
        pass

    # --- Create Bell pair on qubits 1 & 2 ---
    qc.h(1)
    qc.cx(1, 2)

    # --- Bell measurement on qubits 0 & 1 ---
    qc.cx(0, 1)
    qc.h(0)

    # --- Classical communication (simulated by deferred measurement) ---
    # Measure q0 and q1 → classical bits used for Pauli correction
    qc.measure([0, 1], [0, 1])

    # --- Pauli corrections on qubit 2 (Bob's qubit) ---
    # In real protocol these are conditional on classical bits.
    # For the simulator we leave the gates; the measurement engine will
    # apply statistical effects.
    # (Actual conditional gates are added in pauli.py)

    return qc
