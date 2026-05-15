"""Задание 5 (как health_score в MetLab12): индекс привлекательности номера."""

from app.models.room import RoomStatus, RoomType


def calculate_room_attractiveness_score(
    *,
    price_per_night: float,
    room_type: RoomType,
    status: RoomStatus,
    capacity: int,
    floor: int,
) -> int:
    """
    0–100: чем выше, тем «лучше» номер для продажи.
    Учитывает тип, цену, этаж, вместимость и доступность.
    """
    score = 40

    type_bonus = {
        RoomType.standard: 5,
        RoomType.deluxe: 12,
        RoomType.suite: 20,
    }
    score += type_bonus.get(room_type, 0)

    if 3000 <= price_per_night <= 8000:
        score += 15
    elif price_per_night < 3000:
        score += 8
    else:
        score += 10

    if status == RoomStatus.available:
        score += 18
    elif status == RoomStatus.cleaning:
        score += 6
    elif status == RoomStatus.occupied:
        score += 2
    else:
        score -= 10

    score += min(capacity * 3, 12)
    if 2 <= floor <= 8:
        score += 8
    elif floor > 8:
        score += 4

    return max(0, min(score, 100))
