"""
Задание 1: CRUD REST API для сущности «Номер отеля» (/items).
По образцу MetLab12: GET без ключа, POST/PUT/DELETE с X-API-Key.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import EntityNotFoundError
from app.models.room import Room
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.security_api import require_api_key

router = APIRouter(prefix="/items", tags=["items"])


def _get_room_or_404(db: Session, item_id: int) -> Room:
    room = db.query(Room).filter(Room.id == item_id).first()
    if not room:
        raise EntityNotFoundError("Room", item_id)
    return room


@router.get("", response_model=list[ItemResponse])
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[ItemResponse]:
    rooms = db.query(Room).order_by(Room.id).offset(skip).limit(limit).all()
    return [ItemResponse.from_room(r) for r in rooms]


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ItemResponse:
    return ItemResponse.from_room(_get_room_or_404(db, item_id))


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    data: ItemCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_api_key),
) -> ItemResponse:
    if db.query(Room).filter(Room.number == data.number).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Room number already exists")
    room = Room(**data.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return ItemResponse.from_room(room)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    data: ItemUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_api_key),
) -> ItemResponse:
    room = _get_room_or_404(db, item_id)
    payload = data.model_dump(exclude_unset=True)
    if "number" in payload and payload["number"] != room.number:
        if db.query(Room).filter(Room.number == payload["number"], Room.id != item_id).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Number already in use")
    for key, value in payload.items():
        setattr(room, key, value)
    db.commit()
    db.refresh(room)
    return ItemResponse.from_room(room)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_api_key),
) -> Response:
    room = _get_room_or_404(db, item_id)
    if room.bookings:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete room with active bookings",
        )
    db.delete(room)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
