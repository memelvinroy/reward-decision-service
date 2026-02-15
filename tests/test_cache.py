import pytest

from app.cache.memory_cache import MemoryCache
from app.core.config import PolicyConfig
from app.models.request import RewardRequest
from app.services.reward_service import RewardService


@pytest.mark.asyncio
async def test_daily_cac_cap_enforced():
    cache = MemoryCache()
    config = PolicyConfig("config/policy.yaml")

    # Increase cap temporarily for predictable test
    config.daily_cac_cap["NEW"] = 500

    service = RewardService(config=config, cache=cache)

    request1 = RewardRequest(
        txn_id="txn1",
        user_id="user_new",
        merchant_id="m1",
        amount=100,
        txn_type="ONLINE",
        ts=1700000000,
    )

    request2 = RewardRequest(
        txn_id="txn2",
        user_id="user_new",
        merchant_id="m1",
        amount=100,
        txn_type="ONLINE",
        ts=1700000000,
    )

    await service.decide(request1)
    response2 = await service.decide(request2)

    assert "CAC_CAP_EXCEEDED" in response2.reason_codes