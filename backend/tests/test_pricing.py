from datetime import date

import pytest

from app.services.pricing import calculate_stay_price


def test_basic_stay():
    r = calculate_stay_price(1000, date(2026, 6, 1), date(2026, 6, 4))
    assert r.nights == 3
    assert r.base_total == 3000
    assert r.final_total == 3000


def test_long_stay_discount():
    r = calculate_stay_price(1000, date(2026, 6, 1), date(2026, 6, 9))
    assert r.nights == 8
    assert r.discount_percent == 10


def test_invalid_dates():
    with pytest.raises(ValueError):
        calculate_stay_price(1000, date(2026, 6, 5), date(2026, 6, 5))
