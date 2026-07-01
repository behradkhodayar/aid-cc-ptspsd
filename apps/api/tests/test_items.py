"""Tests for the example items resource."""

from httpx import AsyncClient


async def test_create_and_fetch_item(client: AsyncClient) -> None:
    created = await client.post("/items", json={"name": "widget", "description": "a test item"})
    assert created.status_code == 201
    item = created.json()
    assert item["id"] > 0
    assert item["name"] == "widget"

    fetched = await client.get(f"/items/{item['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "widget"


async def test_list_items(client: AsyncClient) -> None:
    await client.post("/items", json={"name": "one"})
    await client.post("/items", json={"name": "two"})
    resp = await client.get("/items")
    assert resp.status_code == 200
    names = {i["name"] for i in resp.json()}
    assert {"one", "two"} <= names


async def test_missing_item_returns_404(client: AsyncClient) -> None:
    resp = await client.get("/items/999999")
    assert resp.status_code == 404


async def test_create_item_validation(client: AsyncClient) -> None:
    resp = await client.post("/items", json={"name": ""})
    assert resp.status_code == 422
