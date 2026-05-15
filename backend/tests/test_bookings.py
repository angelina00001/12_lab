from datetime import date, timedelta

from tests.conftest import auth_header


def test_create_booking(client, staff_token):
    rooms = client.get("/api/rooms", headers=auth_header(staff_token)).json()
    guests = client.get("/api/guests", headers=auth_header(staff_token)).json()
    check_in = date.today() + timedelta(days=10)
    check_out = check_in + timedelta(days=3)
    r = client.post(
        "/api/bookings",
        headers=auth_header(staff_token),
        json={
            "room_id": rooms[0]["id"],
            "guest_id": guests[0]["id"],
            "check_in": str(check_in),
            "check_out": str(check_out),
        },
    )
    assert r.status_code == 201
    assert r.json()["total_price"] > 0
    assert r.json()["nights"] == 3


def test_booking_invalid_dates(client, staff_token):
    rooms = client.get("/api/rooms", headers=auth_header(staff_token)).json()
    guests = client.get("/api/guests", headers=auth_header(staff_token)).json()
    today = date.today()
    r = client.post(
        "/api/bookings",
        headers=auth_header(staff_token),
        json={
            "room_id": rooms[0]["id"],
            "guest_id": guests[0]["id"],
            "check_in": str(today),
            "check_out": str(today),
        },
    )
    assert r.status_code == 422


def test_overlapping_booking_rejected(client, staff_token):
    rooms = client.get("/api/rooms", headers=auth_header(staff_token)).json()
    guests = client.get("/api/guests", headers=auth_header(staff_token)).json()
    check_in = date.today() + timedelta(days=20)
    check_out = check_in + timedelta(days=2)
    payload = {
        "room_id": rooms[1]["id"],
        "guest_id": guests[0]["id"],
        "check_in": str(check_in),
        "check_out": str(check_out),
    }
    assert client.post("/api/bookings", headers=auth_header(staff_token), json=payload).status_code == 201
    overlap = client.post("/api/bookings", headers=auth_header(staff_token), json=payload)
    assert overlap.status_code == 400
