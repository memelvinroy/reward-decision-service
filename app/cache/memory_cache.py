import time
from typing import Dict, Optional

from app.cache.base import CacheBase


class MemoryCache(CacheBase):
    def __init__(self):
        self._store: Dict[str, str] = {}
        self._expiry: Dict[str, float] = {}

    async def get(self, key: str) -> Optional[str]:
        if key in self._store:
            if self._expiry[key] > time.time():
                return self._store[key]
            self._store.pop(key, None)
            self._expiry.pop(key, None)
        return None

    async def set(self, key: str, value: str, ttl: int) -> None:
        self._store[key] = value
        self._expiry[key] = time.time() + ttl