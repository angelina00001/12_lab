"""
Задание 5: расчёт стоимости проживания со скидками, штрафами и сезонной наценкой.
"""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class PricingResult:
    nights: int
    base_total: float
    discount_percent: float
    discount_amount: float
    surcharge_amount: float
    penalty_amount: float
    final_total: float
    breakdown: list[str]


def calculate_stay_price(
    price_per_night: float,
    check_in: date,
    check_out: date,
    *,
    is_loyalty_guest: bool = False,
    late_checkout_hours: int = 0,
    is_peak_season: bool = False,
) -> PricingResult:
    """
    Бизнес-логика:
    - база = цена × ночи;
    - скидка 10% при ≥7 ночах, +5% для постоянных гостей (не более 20% суммарно);
    - наценка 15% в пиковый сезон;
    - штраф 500 ₽/час за поздний выезд сверх 2 часов включённого времени.
    """
    nights = (check_out - check_in).days
    if nights <= 0:
        raise ValueError("check_out must be after check_in")

    base = round(price_per_night * nights, 2)
    breakdown: list[str] = [f"База: {price_per_night} × {nights} = {base}"]

    discount_pct = 0.0
    if nights >= 7:
        discount_pct += 10.0
        breakdown.append("Скидка за длительное проживание (≥7 ночей): 10%")
    if is_loyalty_guest:
        discount_pct += 5.0
        breakdown.append("Скидка постоянного гостя: +5%")
    discount_pct = min(discount_pct, 20.0)
    discount_amount = round(base * discount_pct / 100, 2)

    surcharge = round(base * 0.15, 2) if is_peak_season else 0.0
    if surcharge:
        breakdown.append("Пиковый сезон: +15% к базе")

    free_late_hours = 2
    penalty = 0.0
    if late_checkout_hours > free_late_hours:
        billable = late_checkout_hours - free_late_hours
        penalty = round(billable * 500, 2)
        breakdown.append(f"Штраф за поздний выезд: {billable} ч × 500 = {penalty}")

    final = round(base - discount_amount + surcharge + penalty, 2)
    return PricingResult(
        nights=nights,
        base_total=base,
        discount_percent=discount_pct,
        discount_amount=discount_amount,
        surcharge_amount=surcharge,
        penalty_amount=penalty,
        final_total=final,
        breakdown=breakdown,
    )
