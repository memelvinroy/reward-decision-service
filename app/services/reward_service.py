from datetime import datetime
from typing import List

from app.cache.base import CacheBase
from app.core.config import PolicyConfig
from app.core.persona import get_persona
from app.core.policy import calculate_xp
from app.models.request import RewardRequest
from app.models.response import RewardResponse
from app.utils.idempotency import (
    generate_decision_id,
    generate_idempotency_key,
)


class RewardService:
    def __init__(self, config: PolicyConfig, cache: CacheBase):
        self.config = config
        self.cache = cache

    async def decide(self, request: RewardRequest) -> RewardResponse:
        idem_key = generate_idempotency_key(
            request.txn_id,
            request.user_id,
            request.merchant_id,
        )

        # Idempotency check
        cached = await self.cache.get(idem_key)
        if cached:
            return RewardResponse.model_validate_json(cached)
        #  Persona lookup
        persona = get_persona(request.user_id)
        multiplier = self.config.persona_multipliers[persona]
        print("Recomputing reward logic")

        #  XP calculation
        xp = calculate_xp(
            request.amount,
            self.config.xp_per_rupee,
            multiplier,
            self.config.max_xp_per_txn,
        )

        reward_type = "XP"
        reward_value = xp
        reason_codes: List[str] = []

        #  Daily CAC cap enforcement
        today = datetime.utcnow().strftime("%Y-%m-%d")
        cac_key = f"cac:{request.user_id}:{today}"

        current_cac = await self.cache.get(cac_key)
        current_cac = int(current_cac) if current_cac else 0

        cap = self.config.daily_cac_cap[persona]

        if current_cac + reward_value > cap:
            reason_codes.append("CAC_CAP_EXCEEDED")
        else:
            await self.cache.set(
                cac_key,
                str(current_cac + reward_value),
                86400,
            )

        #  Deterministic decision_id
        decision_id = generate_decision_id(
            request.txn_id,
            request.user_id,
            request.merchant_id,
            self.config.policy_version,
        )

        response = RewardResponse(
            decision_id=decision_id,
            policy_version=self.config.policy_version,
            reward_type=reward_type,
            reward_value=reward_value,
            xp=xp,
            reason_codes=reason_codes,
            meta={"persona": persona},
        )

        # Store idempotency result
        await self.cache.set(
            idem_key,
            response.model_dump_json(),
            self.config.idempotency_ttl_seconds,
        )

        return response