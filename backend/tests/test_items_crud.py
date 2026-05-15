"""Задание 2: pytest для CRUD /items и граничных случаев (как test_clients_api в MetLab12)."""

import os

import pytest

API_KEY = os.environ.get("API_KEY", "change-me-for-local-dev")
WRITE_HEADERS = {"X-API-Key": API_KEY}

VALID_ROOM = {
    "number": "AB-3-12",
    "room_type": "standard",
    "price_per_night": 3500.0,
    "capacity": 2,
    "floor": 3,
    "description": "Вид на город",
    "status": "available",
}


def test_create_item(client):
    r = client.post("/items", json=VALID_ROOM, headers=WRITE_HEADERS)
    assert r.status_code == 201
    body = r.json()
    assert body["id"] > 0
    assert body["number"] == "AB-3-12"
    assert body["price_per_night"] == 3500.0


def test_list_items(client):
    client.post("/items", json=VALID_ROOM, headers=WRITE_HEADERS)
    r = client.get("/items")
    assert r.status_code == 200
    assert len(r.json()) >= 1


def test_get_item(client):
    created = client.post("/items", json=VALID_ROOM, headers=WRITE_HEADERS).json()
    r = client.get(f"/items/{created['id']}")
    assert r.status_code == 200
    assert r.json()["number"] == "AB-3-12"


def test_get_item_not_found(client):
    r = client.get("/items/99999")
    assert r.status_code == 404


def test_update_item(client):
    created = client.post("/items", json=VALID_ROOM, headers=WRITE_HEADERS).json()
    r = client.put(
        f"/items/{created['id']}",
        json={"price_per_night": 4000.0, "description": "Обновлено"},
        headers=WRITE_HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["price_per_night"] == 4000.0
    assert r.json()["description"] == "Обновлено"


def test_delete_item(client):
    created = client.post("/items", json=VALID_ROOM, headers=WRITE_HEADERS).json()
    r = client.delete(f"/items/{created['id']}", headers=WRITE_HEADERS)
    assert r.status_code == 204
    assert client.get(f"/items/{created['id']}").status_code == 404


def test_invalid_room_code(client):
    bad = {**VALID_ROOM, "number": "invalid-code"}
    r = client.post("/items", json=bad, headers=WRITE_HEADERS)
    assert r.status_code == 422


def test_negative_price(client):
    bad = {**VALID_ROOM, "price_per_night": -100}
    r = client.post("/items", json=bad, headers=WRITE_HEADERS)
    assert r.status_code == 422


def test_duplicate_number(client):
    client.post("/items", json=VALID_ROOM, headers=WRITE_HEADERS)
    r = client.post("/items", json=VALID_ROOM, headers=WRITE_HEADERS)
    assert r.status_code == 409


def test_write_requires_api_key(client):
    r = client.post("/items", json=VALID_ROOM)
    assert r.status_code == 401


@pytest.mark.parametrize(
    "number,expected",
    [
        ("AB-3-12", True),
        ("A-1-05", True),
        ("XY-12-999", True),
        ("ab-3-12", True),
        ("AB312", False),
        ("AB-3", False),
        ("123-45-67", False),
    ],
)
def test_room_code_regex(number, expected):
    from app.schemas.item import ROOM_CODE_PATTERN

    assert bool(ROOM_CODE_PATTERN.match(number.strip().upper())) is expected
