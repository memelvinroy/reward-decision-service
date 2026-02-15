import pytest

from app.cache.memory_cache import MemoryCache
from app.core.config import PolicyConfig
from app.models.request import RewardRequest
from app.services.reward_service import RewardService


@pytest.mark.asyncio
async def test_idempotent_request_returns_same_result():
    cache = MemoryCache()
    config = PolicyConfig("config/policy.yaml")
    service = RewardService(config=config, cache=cache)

    request = RewardRequest(
        txn_id="txn1",
        user_id="user_new",
        merchant_id="m1",
        amount=100,
        txn_type="ONLINE",
        ts=1700000000,
    )

    response1 = await service.decide(request)
    response2 = await service.decide(request)

    assert response1.decision_id == response2.decision_id
    assert response1.reward_value == response2.reward_value
    assert response1.xp == response2.xp