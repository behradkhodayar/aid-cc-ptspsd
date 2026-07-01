"""Shared pytest fixtures. Tests run against the DATABASE_URL Postgres (compose or CI service)."""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings
from app.db import Base, get_session
from app.main import app


@pytest.fixture(scope="session")
async def engine() -> AsyncGenerator[object]:
    """Create the schema once per test session, tearing it down at the end."""
    eng = create_async_engine(get_settings().database_url, poolclass=None)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await eng.dispose()


@pytest.fixture
async def client(engine: object) -> AsyncGenerator[AsyncClient]:
    """HTTP client wired to the app, with each test in its own rolled-back transaction."""
    factory = async_sessionmaker(engine, expire_on_commit=False)  # type: ignore[arg-type]

    async def override_get_session() -> AsyncGenerator[AsyncSession]:
        async with factory() as session:
            yield session
            await session.commit()

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
