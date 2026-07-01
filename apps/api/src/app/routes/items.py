"""CRUD routes for the example `items` resource. Replace with real domain routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Item
from app.schemas import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=list[ItemRead])
async def list_items(session: SessionDep) -> list[Item]:
    """Return all items, newest first."""
    result = await session.execute(select(Item).order_by(Item.created_at.desc()))
    return list(result.scalars().all())


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate, session: SessionDep) -> Item:
    """Create a new item."""
    item = Item(name=payload.name, description=payload.description)
    session.add(item)
    await session.flush()
    await session.refresh(item)
    return item


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, session: SessionDep) -> Item:
    """Fetch a single item by id, or 404 if it does not exist."""
    item = await session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item
