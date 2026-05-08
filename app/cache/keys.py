from __future__ import annotations

import hashlib
import json
from typing import Any, Final

PREFIX: Final[str] = "trading"


def dates_key(last_days: int) -> str:
    return f"{PREFIX}:dates:last_days:{last_days}"


def dynamics_key(params_hash: str) -> str:
    return f"{PREFIX}:dynamics:{params_hash}"


def results_key(params_hash: str) -> str:
    return f"{PREFIX}:results:{params_hash}"


def hash_params(payload: dict[str, Any]) -> str:
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
