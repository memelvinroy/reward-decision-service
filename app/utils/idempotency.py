import hashlib


def generate_idempotency_key(
    txn_id: str,
    user_id: str,
    merchant_id: str,
) -> str:
    return f"idem:{txn_id}:{user_id}:{merchant_id}"


def generate_decision_id(
    txn_id: str,
    user_id: str,
    merchant_id: str,
    policy_version: str,
) -> str:
    raw = f"{txn_id}:{user_id}:{merchant_id}:{policy_version}"
    return hashlib.sha256(raw.encode()).hexdigest()