from datetime import date, datetime, timedelta, timezone

from tests.conftest import auth_header


def _create_booking(client, token):
    rooms = client.get("/api/rooms", headers=auth_header(token)).json()
    guests = client.get("/api/guests", headers=auth_header(token)).json()
    check_in = date.today()
    check_out = check_in + timedelta(days=1)
    return client.post(
        "/api/bookings",
        headers=auth_header(token),
        json={
            "room_id": rooms[2]["id"],
            "guest_id": guests[1]["id"],
            "check_in": str(check_in),
            "check_out": str(check_out),
        },
    ).json()


def test_check_in_and_out_flow(client, staff_token):
    booking = _create_booking(client, staff_token)
    check_in = client.post(
        "/api/stays/check-in",
        headers=auth_header(staff_token),
        json={"booking_id": booking["id"]},
    )
    assert check_in.status_code == 201
    stay_id = check_in.json()["id"]
    check_out = client.post(f"/api/stays/{stay_id}/check-out", headers=auth_header(staff_token))
    assert check_out.status_code == 200
    assert check_out.json()["status"] == "completed"


def test_cleaning_complete(client, staff_token):
    rooms = client.get("/api/rooms", headers=auth_header(staff_token)).json()
    room = next(r for r in rooms if r["status"] == "cleaning") if any(r["status"] == "cleaning" for r in rooms) else rooms[0]
    scheduled = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    task = client.post(
        "/api/cleaning",
        headers=auth_header(staff_token),
        json={"room_id": room["id"], "scheduled_at": scheduled},
    )
    assert task.status_code == 201
    task_id = task.json()["id"]
    done = client.post(f"/api/cleaning/{task_id}/complete", headers=auth_header(staff_token))
    assert done.status_code == 200
    assert done.json()["status"] == "completed"
