from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Machine, Zone

router = APIRouter(prefix="/api/about", tags=["О 5 этаже"])


@router.get("")
def about(db: Session = Depends(get_db)):
    """Общая информация для главной страницы."""
    return {
        "title": settings.floor_title,
        "description": settings.floor_description,
        "hours": settings.floor_hours,
        "contact": settings.floor_contact,
        "zones_count": db.scalar(select(func.count(Zone.id))),
        "machines_total": db.scalar(select(func.coalesce(func.sum(Machine.quantity), 0))),
    }
