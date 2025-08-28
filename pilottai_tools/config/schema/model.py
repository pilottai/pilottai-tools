from typing import Optional, Dict, Any, Set, Type
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from pilottai_tools.source.base.base_input import BaseInputSource


class KnowledgeSource(BaseModel):
    name: str
    type: Type[BaseInputSource]
    connection: Dict[str, Any]
    last_access: datetime = Field(default_factory=datetime.now)
    access_count: int = 0
    error_count: int = 0
    is_connected: bool = False
    max_retries: int = 3
    retry_delay: int = 5
    timeout: int = 30

class MemoryItem(BaseModel):
    """Enhanced memory item model"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    tags: Set[str] = Field(default_factory=set)
    priority: int = Field(ge=0, default=0)
    expires_at: Optional[datetime] = None
    version: int = 1

    def is_expired(self) -> bool:
        return self.expires_at and datetime.now() > self.expires_at



class MemoryEntry(BaseModel):
    """Enhanced memory entry with job awareness"""
    text: str
    entry_type: str  # 'job', 'context', 'result', etc.
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    tags: Set[str] = Field(default_factory=set)
    priority: int = Field(ge=0, default=1)
    job_id: Optional[str] = None
    agent_id: Optional[str] = None


class CacheEntry(BaseModel):
    value: Any
    timestamp: datetime
    ttl: int
    access_count: int = 0
    last_access: datetime = Field(default_factory=datetime.now)





