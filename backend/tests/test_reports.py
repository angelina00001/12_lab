from datetime import date, timedelta

from tests.conftest import auth_header


def test_reports_require_staff(client, admin_token):
    today = date.today()
    from_d = today - timedelta(days=7)
    r = client.get(
        f"/api/reports/occupancy?from={from_d}&to={today}",
        headers=auth_header(admin_token),
    )
    assert r.status_code == 200
    data = r.json()
    assert "occupancy_rate_percent" in data
    assert "total_rooms" in data


def test_revenue_report(client, staff_token):
    today = date.today()
    r = client.get(
        f"/api/reports/revenue?from={today - timedelta(days=30)}&to={today}",
        headers=auth_header(staff_token),
    )
    assert r.status_code == 200
    assert "total_revenue" in r.json()
