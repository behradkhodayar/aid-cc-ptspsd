"""Pydantic request/response models — the HTTP contract with the web client."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    """Payload for creating an item."""

    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)


class ItemRead(BaseModel):
    """Item as returned to clients."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class HealthStatus(BaseModel):
    """Response of the health endpoints."""

    status: str
    database: bool
