"""
Timestamp freshness check.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Tuple
from dateutil import parser


ALLOWED_WINDOW_MINUTES = 15


def check_timestamp(package: Dict[str, Any]) -> Tuple[bool, str]:
    ts_str = package.get("timestamp")
    if not ts_str:
        return False, "Missing timestamp"

    try:
        # Handle trailing Z
        ts = parser.isoparse(ts_str.replace("Z", "+00:00"))
    except Exception:
        return False, "Invalid timestamp format"

    now = datetime.utcnow().replace(tzinfo=ts.tzinfo)
    delta = abs(now - ts)

    if delta > timedelta(minutes=ALLOWED_WINDOW_MINUTES):
        return False, f"Timestamp outside allowed window ({ALLOWED_WINDOW_MINUTES} min). Age: {delta}"

    return True, "Timestamp valid"
