from tests.conftest import auth_header


def test_list_rooms(client, staff_token):
    r = client.get("/api/rooms", headers=auth_header(staff_token))
    assert r.status_code == 200
    assert len(r.json()) >= 4


def test_create_room(client, staff_token):
    r = client.post(
        "/api/rooms",
        headers=auth_header(staff_token),
        json={
            "number": "D-9-99",
            "room_type": "standard",
            "price_per_night": 4000,
            "capacity": 2,
            "floor": 9,
        },
    )
    assert r.status_code == 201
    assert r.json()["number"] == "D-9-99"


def test_create_room_negative_price_rejected(client, staff_token):
    r = client.post(
        "/api/rooms",
        headers=auth_header(staff_token),
        json={
            "number": "998",
            "room_type": "standard",
            "price_per_night": -100,
            "capacity": 2,
            "floor": 9,
        },
    )
    assert r.status_code == 422


def test_guest_cannot_create_room(client, admin_token):
    reg = client.post(
        "/api/auth/register",
        json={
            "email": "onlyguest@test.com",
            "full_name": "Гость",
            "password": "password1",
            "role": "guest",
        },
    )
    assert reg.status_code == 201
    login = client.post(
        "/api/auth/login",
        data={"username": "onlyguest@test.com", "password": "password1"},
    )
    token = login.json()["access_token"]
    r = client.post(
        "/api/rooms",
        headers=auth_header(token),
        json={
            "number": "997",
            "room_type": "standard",
            "price_per_night": 3000,
            "capacity": 2,
            "floor": 1,
        },
    )
    assert r.status_code == 403
