"""
Bell-state preparation for Teleportation-QDS.
Creates the entangled pair |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
"""

from qiskit import QuantumCircuit


def create_bell_pair() -> QuantumCircuit:
    """
    Standard Bell pair circuit on qubits 0 and 1.
    """
    qc = QuantumCircuit(2, name="Bell_Phi+")
    qc.h(0)
    qc.cx(0, 1)
    return qc


def create_bell_circuit_for_teleport() -> QuantumCircuit:
    """
    3-qubit circuit used inside teleportation:
    q0 = state to teleport
    q1, q2 = Bell pair
    """
    qc = QuantumCircuit(3, 3, name="Teleport_Bell")
    # Bell pair on q1-q2
    qc.h(1)
    qc.cx(1, 2)
    return qc
