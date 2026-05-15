"""Дополнительные тесты для покрытия ≥85% (задание 7)."""

from datetime import date, datetime, timedelta, timezone

import pytest

from app.auth.security import decode_access_token, get_password_hash
from app.models.room import RoomStatus
from tests.conftest import auth_header


def test_get_and_update_room(client, staff_token):
    rooms = client.get("/api/rooms", headers=auth_header(staff_token)).json()
    room_id = rooms[0]["id"]
    assert client.get(f"/api/rooms/{room_id}", headers=auth_header(staff_token)).status_code == 200
    updated = client.patch(
        f"/api/rooms/{room_id}",
        headers=auth_header(staff_token),
        json={"description": "Обновлён"},
    )
    assert updated.status_code == 200
    assert updated.json()["description"] == "Обновлён"


def test_room_not_found(client, staff_token):
    assert client.get("/api/rooms/99999", headers=auth_header(staff_token)).status_code == 404


def test_room_duplicate_number(client, staff_token):
    rooms = client.get("/api/rooms", headers=auth_header(staff_token)).json()
    r = client.post(
        "/api/rooms",
        headers=auth_header(staff_token),
        json={
            "number": rooms[0]["number"],
            "room_type": "standard",
            "price_per_night": 1000,
            "capacity": 2,
            "floor": 1,
        },
    )
    assert r.status_code == 400


def test_rooms_filter_by_status(client, staff_token):
    r = client.get("/api/rooms?status=available", headers=auth_header(staff_token))
    assert r.status_code == 200
    assert all(x["status"] == "available" for x in r.json())


def test_guest_update_and_not_found(client, staff_token):
    guests = client.get("/api/guests", headers=auth_header(staff_token)).json()
    gid = guests[0]["id"]
    assert (
        client.patch(
            f"/api/guests/{gid}",
            headers=auth_header(staff_token),
            json={"phone": "+79991112233"},
        ).status_code
        == 200
    )
    assert client.patch("/api/guests/99999", headers=auth_header(staff_token), json={"phone": "x"}).status_code == 404


def test_guest_duplicate_email(client, staff_token):
    guests = client.get("/api/guests", headers=auth_header(staff_token)).json()
    email = guests[0]["email"]
    r = client.post(
        "/api/guests",
        headers=auth_header(staff_token),
        json={"full_name": "Дубликат", "email": email},
    )
    assert r.status_code == 400


def test_booking_cancel_and_update(client, staff_token):
    bookings = client.get("/api/bookings", headers=auth_header(staff_token)).json()
    if not bookings:
        pytest.skip("no bookings")
    bid = bookings[0]["id"]
    cancelled = client.post(f"/api/bookings/{bid}/cancel", headers=auth_header(staff_token))
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    assert client.post("/api/bookings/99999/cancel", headers=auth_header(staff_token)).status_code == 404


def test_booking_update_not_found(client, staff_token):
    r = client.patch(
        "/api/bookings/99999",
        headers=auth_header(staff_token),
        json={"notes": "x"},
    )
    assert r.status_code == 404


def test_booking_list_with_status(client, staff_token):
    r = client.get("/api/bookings?status=confirmed", headers=auth_header(staff_token))
    assert r.status_code == 200


def test_booking_maintenance_room(client, staff_token, db_session):
    from app.models.room import Room, RoomType

    room = Room(number="MNT1", room_type=RoomType.standard, price_per_night=1000, capacity=1, status=RoomStatus.maintenance)
    db_session.add(room)
    db_session.commit()
    guests = client.get("/api/guests", headers=auth_header(staff_token)).json()
    check_in = date.today() + timedelta(days=40)
    check_out = check_in + timedelta(days=2)
    r = client.post(
        "/api/bookings",
        headers=auth_header(staff_token),
        json={
            "room_id": room.id,
            "guest_id": guests[0]["id"],
            "check_in": str(check_in),
            "check_out": str(check_out),
        },
    )
    assert r.status_code == 400


def test_admin_set_role_and_deactivate(client, admin_token):
    reg = client.post(
        "/api/auth/register",
        json={
            "email": "roletest@example.com",
            "full_name": "Role Test",
            "password": "password1",
            "role": "guest",
        },
    )
    assert reg.status_code == 201
    uid = reg.json()["id"]
    assert client.patch(
        f"/api/admin/users/{uid}/role?role=staff",
        headers=auth_header(admin_token),
    ).status_code == 200
    me = client.get("/api/auth/me", headers=auth_header(admin_token)).json()
    assert client.patch(f"/api/admin/users/{me['id']}/deactivate", headers=auth_header(admin_token)).status_code == 400
    assert client.patch("/api/admin/users/99999/role?role=staff", headers=auth_header(admin_token)).status_code == 404


def test_admin_deactivate_user(client, admin_token):
    reg = client.post(
        "/api/auth/register",
        json={
            "email": "deact@example.com",
            "full_name": "Deactivate Me",
            "password": "password1",
            "role": "guest",
        },
    )
    assert reg.status_code == 201
    uid = reg.json()["id"]
    assert client.patch(f"/api/admin/users/{uid}/deactivate", headers=auth_header(admin_token)).status_code == 200


def test_register_duplicate(client):
    payload = {
        "email": "dup@example.com",
        "full_name": "Dup",
        "password": "password1",
        "role": "guest",
    }
    assert client.post("/api/auth/register", json=payload).status_code == 201
    assert client.post("/api/auth/register", json=payload).status_code == 400


def test_decode_token_invalid():
    assert decode_access_token("not-a-token") is None


def test_reports_cleaning_and_stays(client, staff_token):
    assert client.get("/api/reports/cleaning", headers=auth_header(staff_token)).status_code == 200
    assert client.get("/api/reports/stays", headers=auth_header(staff_token)).status_code == 200


def test_cleaning_create_and_update(client, staff_token):
    rooms = client.get("/api/rooms", headers=auth_header(staff_token)).json()
    scheduled = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()
    created = client.post(
        "/api/cleaning",
        headers=auth_header(staff_token),
        json={"room_id": rooms[0]["id"], "scheduled_at": scheduled, "notes": "test"},
    )
    assert created.status_code == 201
    tid = created.json()["id"]
    updated = client.patch(
        f"/api/cleaning/{tid}",
        headers=auth_header(staff_token),
        json={"notes": "updated"},
    )
    assert updated.status_code == 200
    assert client.patch("/api/cleaning/99999", headers=auth_header(staff_token), json={"notes": "x"}).status_code == 404


def test_stays_list(client, staff_token):
    assert client.get("/api/stays", headers=auth_header(staff_token)).status_code == 200


def test_inactive_user_login(client, db_session):
    from app.models.user import User, UserRole

    user = User(
        email="inactive@example.com",
        full_name="Inactive",
        hashed_password=get_password_hash("password1"),
        role=UserRole.guest,
        is_active=False,
    )
    db_session.add(user)
    db_session.commit()
    r = client.post(
        "/api/auth/login",
        data={"username": "inactive@example.com", "password": "password1"},
    )
    assert r.status_code == 403
