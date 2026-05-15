from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.deps import RequireStaff
from app.database import get_db
from app.services import reports

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/occupancy")
def occupancy(
    from_date: date | None = Query(None, alias="from"),
    to_date: date | None = Query(None, alias="to"),
    db: Session = Depends(get_db),
    _: object = RequireStaff,
):
    to_d = to_date or date.today()
    from_d = from_date or (to_d - timedelta(days=30))
    return reports.occupancy_report(db, from_d, to_d)


@router.get("/revenue")
def revenue(
    from_date: date | None = Query(None, alias="from"),
    to_date: date | None = Query(None, alias="to"),
    db: Session = Depends(get_db),
    _: object = RequireStaff,
):
    to_d = to_date or date.today()
    from_d = from_date or (to_d - timedelta(days=30))
    return reports.revenue_report(db, from_d, to_d)


@router.get("/cleaning")
def cleaning(db: Session = Depends(get_db), _: object = RequireStaff):
    return reports.cleaning_report(db)


@router.get("/stays")
def stays(db: Session = Depends(get_db), _: object = RequireStaff):
    return reports.stays_summary(db)
