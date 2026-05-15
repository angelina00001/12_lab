from tests.conftest import auth_header


def test_list_guests(client, staff_token):
    r = client.get("/api/guests", headers=auth_header(staff_token))
    assert r.status_code == 200
    assert len(r.json()) >= 1


def test_create_guest(client, staff_token):
    r = client.post(
        "/api/guests",
        headers=auth_header(staff_token),
        json={"full_name": "Тест Гость", "email": "testguest@example.com", "phone": "+7999"},
    )
    assert r.status_code == 201
    assert r.json()["full_name"] == "Тест Гость"
