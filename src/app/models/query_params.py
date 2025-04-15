from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field


class SortDirection(str, Enum):
    ascending = "ascending"
    descending = "descending"


class UserQueryParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)
    sortBy: Optional[str] = None
    sortDirection: SortDirection = SortDirection.ascending
    match: Optional[Dict[str, str]] = Field(default_factory=dict)
