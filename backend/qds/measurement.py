"""
Measurement + basic count analysis for QDS verification.
"""

from qiskit import transpile
from qiskit_aer import AerSimulator
from typing import Dict, Any
import numpy as np


def measure_and_analyze(qc, shots: int = 1024) -> Dict[str, Any]:
    """
    Run the circuit on AerSimulator and return counts + probabilities.
    """
    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    job = simulator.run(compiled, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Normalize to full 3-bit keys (or 2-bit depending on circuit)
    # For our circuits we have 3 classical bits
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    # Aggregate to 2-bit view (last two bits or first two – for demo we use all)
    # Simplified: look at the measured Bob qubit + relevant bits
    two_bit_counts = {"00": 0, "01": 0, "10": 0, "11": 0}
    for bitstring, cnt in counts.items():
        # Take the last two bits (common convention)
        key = bitstring[-2:] if len(bitstring) >= 2 else bitstring.zfill(2)
        if key in two_bit_counts:
            two_bit_counts[key] += cnt
        else:
            two_bit_counts["00"] += cnt  # fallback

    two_bit_probs = {k: v / total for k, v in two_bit_counts.items()}

    return {
        "raw_counts": counts,
        "counts": two_bit_counts,
        "probabilities": two_bit_probs,
        "shots": shots,
        "total": total
    }
