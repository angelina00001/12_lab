"""Задание 3: рефакторинг legacy_bad.calc → делегирование в pricing."""

from datetime import date

from app.services.pricing import PricingResult, calculate_stay_price


def calculate_stay_total(
    price_per_night: float,
    check_in: date,
    check_out: date,
    *,
    is_loyalty_guest: bool = False,
    late_checkout_hours: int = 0,
    is_peak_season: bool = False,
) -> PricingResult:
    return calculate_stay_price(
        price_per_night,
        check_in,
        check_out,
        is_loyalty_guest=is_loyalty_guest,
        late_checkout_hours=late_checkout_hours,
        is_peak_season=is_peak_season,
    )
