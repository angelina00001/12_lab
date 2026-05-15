from tests.conftest import auth_header


def test_register_and_login(client):
    r = client.post(
        "/api/auth/register",
        json={
            "email": "newguest@test.com",
            "full_name": "Новый Гость",
            "password": "password1",
            "role": "guest",
        },
    )
    assert r.status_code == 201
    assert r.json()["email"] == "newguest@test.com"

    login = client.post(
        "/api/auth/login",
        data={"username": "newguest@test.com", "password": "password1"},
    )
    assert login.status_code == 200
    assert "access_token" in login.json()


def test_login_wrong_password(client):
    r = client.post(
        "/api/auth/login",
        data={"username": "admin@hotel.example.com", "password": "wrong"},
    )
    assert r.status_code == 401


def test_me_requires_token(client, admin_token):
    r = client.get("/api/auth/me", headers=auth_header(admin_token))
    assert r.status_code == 200
    assert r.json()["role"] == "admin"


def test_me_without_token(client):
    assert client.get("/api/auth/me").status_code == 401
