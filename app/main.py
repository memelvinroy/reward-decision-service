from fastapi import FastAPI

from app.api.reward import router as reward_router
from app.cache.memory_cache import MemoryCache
from app.core.config import PolicyConfig
from app.services.reward_service import RewardService


app = FastAPI(title="Reward Decision Service")


# Load policy config
config = PolicyConfig("config/policy.yaml")

# Initialize cache (memory for now)
cache = MemoryCache()

# Initialize reward service
reward_service = RewardService(config=config, cache=cache)


# Register routes
app.include_router(reward_router)