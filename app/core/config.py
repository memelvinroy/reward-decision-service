import yaml
from typing import Any, Dict


class PolicyConfig:
    def __init__(self, path: str):
        with open(path, "r") as file:
            data = yaml.safe_load(file)

        self.policy_version: str = data["policy_version"]
        self.reward_type_weights: Dict[str, float] = data["reward_type_weights"]
        self.xp_per_rupee: int = data["xp_per_rupee"]
        self.max_xp_per_txn: int = data["max_xp_per_txn"]
        self.persona_multipliers: Dict[str, float] = data["persona_multipliers"]
        self.daily_cac_cap: Dict[str, int] = data["daily_cac_cap"]
        self.feature_flags: Dict[str, Any] = data["feature_flags"]
        self.idempotency_ttl_seconds: int = data["idempotency_ttl_seconds"]