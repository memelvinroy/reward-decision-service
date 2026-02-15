def calculate_xp(
    amount: float,
    xp_per_rupee: int,
    persona_multiplier: float,
    max_xp_per_txn: int,
) -> int:
    raw_xp = amount * xp_per_rupee * persona_multiplier
    return int(min(raw_xp, max_xp_per_txn))