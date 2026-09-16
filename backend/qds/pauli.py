"""
Pauli correction operators used after teleportation.
"""

from qiskit import QuantumCircuit
from qiskit.circuit.library import XGate, ZGate, YGate


def apply_pauli_correction(qc: QuantumCircuit, correction: str) -> QuantumCircuit:
    """
    Apply the Pauli correction that Bob would apply based on
    the two classical bits received from Alice.
    correction ∈ {"I", "X", "Z", "Y"}
    """
    # Work on a copy so original is not mutated
    new_qc = qc.copy()

    # Bob's qubit is qubit 2
    if correction == "X":
        new_qc.x(2)
    elif correction == "Z":
        new_qc.z(2)
    elif correction == "Y":
        new_qc.y(2)
    # "I" → do nothing

    # Measure Bob's qubit as well (for verification)
    new_qc.measure(2, 2)
    return new_qc


def pauli_from_bits(bit0: int, bit1: int) -> str:
    """Map classical bits to Pauli operator (standard teleportation table)."""
    if bit0 == 0 and bit1 == 0:
        return "I"
    if bit0 == 0 and bit1 == 1:
        return "X"
    if bit0 == 1 and bit1 == 0:
        return "Z"
    return "Y"
