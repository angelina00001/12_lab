from app.models.room import RoomStatus, RoomType
from app.services.room_score import calculate_room_attractiveness_score


def test_suite_room_scores_higher():
    suite = calculate_room_attractiveness_score(
        price_per_night=12000,
        room_type=RoomType.suite,
        status=RoomStatus.available,
        capacity=4,
        floor=5,
    )
    standard = calculate_room_attractiveness_score(
        price_per_night=3500,
        room_type=RoomType.standard,
        status=RoomStatus.maintenance,
        capacity=2,
        floor=1,
    )
    assert suite > standard
