"""
Decision thresholds for quantum verification.
"""

from typing import Dict, Any


# Tunable thresholds for SIH demo
TVD_ACCEPT = 0.12          # Total Variation Distance < this → good
TVD_FLAG = 0.25            # between ACCEPT and FLAG → suspicious
P_VALUE_MIN = 0.01         # chi-square p-value


def decide(stats: Dict[str, Any]) -> str:
    """
    Return one of: ACCEPTED / FLAGGED / REJECTED
    based on statistical metrics.
    """
    tvd = stats.get("total_variation_distance", 1.0)
    p_val = stats.get("p_value", 0.0)

    if tvd <= TVD_ACCEPT and p_val >= P_VALUE_MIN:
        return "ACCEPTED"
    if tvd <= TVD_FLAG:
        return "FLAGGED"
    return "REJECTED"
