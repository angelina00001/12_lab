from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.deps import RequireAdmin
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db), _: User = RequireAdmin):
    return db.query(User).all()


@router.patch("/users/{user_id}/role")
def set_role(
    user_id: int,
    role: UserRole = Query(...),
    db: Session = Depends(get_db),
    _: User = RequireAdmin,
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user.role = role
    db.commit()
    return {"id": user.id, "role": user.role}


@router.patch("/users/{user_id}/deactivate")
def deactivate(user_id: int, db: Session = Depends(get_db), current: User = RequireAdmin):
    if user_id == current.id:
        raise HTTPException(status_code=400, detail="Нельзя деактивировать себя")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user.is_active = False
    db.commit()
    return {"id": user.id, "is_active": False}
