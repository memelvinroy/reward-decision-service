import pytest

from app.core.policy import calculate_xp


def test_basic_xp_calculation():
    xp = calculate_xp(
        amount=100,
        xp_per_rupee=2,
        persona_multiplier=1.0,
        max_xp_per_txn=500,
    )
    assert xp == 200


def test_xp_with_persona_multiplier():
    xp = calculate_xp(
        amount=100,
        xp_per_rupee=2,
        persona_multiplier=1.5,
        max_xp_per_txn=500,
    )
    assert xp == 300


def test_xp_respects_max_cap():
    xp = calculate_xp(
        amount=1000,
        xp_per_rupee=5,
        persona_multiplier=2.0,
        max_xp_per_txn=500,
    )
    assert xp == 500