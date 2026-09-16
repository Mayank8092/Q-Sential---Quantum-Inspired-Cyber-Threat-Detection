"""
Statistical analysis of measurement distributions.
Pure Python / NumPy — no scipy required.
"""

from typing import Dict, Any
import math


def statistical_test(
    expected: Dict[str, float],
    observed_counts: Dict[str, int],
    shots: int
) -> Dict[str, Any]:
    keys = ["00", "01", "10", "11"]

    exp_probs = [float(expected.get(k, 0.0)) for k in keys]
    s = sum(exp_probs)
    if s > 0:
        exp_probs = [p / s for p in exp_probs]

    obs_counts = [float(observed_counts.get(k, 0)) for k in keys]
    obs_probs = [c / shots if shots > 0 else 0.0 for c in obs_counts]

    tvd = 0.5 * sum(abs(e - o) for e, o in zip(exp_probs, obs_probs))
    max_dev = max(abs(e - o) for e, o in zip(exp_probs, obs_probs))

    chi2 = 0.0
    for o, e in zip(obs_counts, exp_probs):
        expected_count = max(e * shots, 1e-6)
        chi2 += (o - expected_count) ** 2 / expected_count

    try:
        p_value = math.exp(-chi2 / 2.0) * (1.0 + chi2 / 2.0)
    except OverflowError:
        p_value = 0.0

    return {
        "total_variation_distance": float(tvd),
        "max_deviation": float(max_dev),
        "chi_square": float(chi2),
        "p_value": float(p_value),
        "expected_probs": {k: float(v) for k, v in zip(keys, exp_probs)},
        "observed_probs": {k: float(v) for k, v in zip(keys, obs_probs)},
        "shots": shots
    }