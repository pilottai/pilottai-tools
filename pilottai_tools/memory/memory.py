import asyncio
from typing import Dict
from datetime import datetime

from pilottai_tools.utils.logger import Logger


class MemoryHandler:
    def __init__(self, cache_size: int = 1000, cache_ttl: int = 3600):
        self.sources: Dict[str, KnowledgeSource] = {}
        self.last_updated: Dict[str, datetime] = {}
        self.source_locks: Dict[str, asyncio.Lock] = {}
        self.cache_lock = asyncio.Lock()
        self.MAX_CACHE_SIZE = max(100, cache_size)
        self.DEFAULT_CACHE_TTL = max(60, cache_ttl)
        self.logger = Logger("MemoryHandler")
        self._setup_logging()
        self._cleanup_task = None

    def _setup_logging(self):
        if not self.logger.handlers:
            handler = self.logger.StreamHandler()
            formatter = self.logger.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(self.logger.INFO)
