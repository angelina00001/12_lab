from tests.conftest import auth_header


def test_admin_list_users(client, admin_token):
    r = client.get("/api/admin/users", headers=auth_header(admin_token))
    assert r.status_code == 200
    assert len(r.json()) >= 2


def test_staff_cannot_access_admin(client, staff_token):
    r = client.get("/api/admin/users", headers=auth_header(staff_token))
    assert r.status_code == 403


def test_health(client):
    assert client.get("/api/health").json()["status"] == "ok"
