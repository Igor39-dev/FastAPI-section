from __future__ import annotations

from app.cache.keys import dates_key, dynamics_key, hash_params, results_key


def test_dates_key_format() -> None:
    assert dates_key(30) == "trading:dates:last_days:30"


def test_dynamics_and_results_key_use_hash_prefix() -> None:
    h = hash_params({"a": 1, "b": 2})
    assert dynamics_key(h) == f"trading:dynamics:{h}"
    assert results_key(h) == f"trading:results:{h}"


def test_hash_params_stable_for_same_payload() -> None:
    p = {"end_date": "2026-01-10", "start_date": "2026-01-01", "z": None, "a": "x"}
    assert hash_params(p) == hash_params(dict(p))


def test_hash_params_order_independent() -> None:
    assert hash_params({"a": 1, "b": 2}) == hash_params({"b": 2, "a": 1})
