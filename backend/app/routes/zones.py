from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import ZoneRepository
from app.schemas import ZoneCreate, ZoneDetail, ZoneOut, ZoneUpdate
from app.security import require_admin

router = APIRouter(prefix="/api/zones", tags=["Зоны"])


def _to_out(zone) -> dict:
    return {
        "id": zone.id,
        "name": zone.name,
        "description": zone.description,
        "machines_count": len(zone.machines),
    }


def _get_or_404(repo: ZoneRepository, zone_id: int):
    zone = repo.get(zone_id)
    if zone is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Зона не найдена")
    return zone


@router.get("", response_model=list[ZoneOut])
def list_zones(db: Session = Depends(get_db)):
    return [_to_out(z) for z in ZoneRepository(db).list()]


@router.get("/{zone_id}", response_model=ZoneDetail)
def get_zone(zone_id: int, db: Session = Depends(get_db)):
    zone = _get_or_404(ZoneRepository(db), zone_id)
    return {**_to_out(zone), "machines": zone.machines}


@router.post("", response_model=ZoneOut, status_code=201, dependencies=[Depends(require_admin)])
def create_zone(payload: ZoneCreate, db: Session = Depends(get_db)):
    repo = ZoneRepository(db)
    if repo.get_by_name(payload.name):
        raise HTTPException(status.HTTP_409_CONFLICT, "Зона с таким названием уже есть")
    return _to_out(repo.create(payload.model_dump()))


@router.put("/{zone_id}", response_model=ZoneOut, dependencies=[Depends(require_admin)])
def update_zone(zone_id: int, payload: ZoneUpdate, db: Session = Depends(get_db)):
    repo = ZoneRepository(db)
    zone = _get_or_404(repo, zone_id)
    data = payload.model_dump(exclude_unset=True)
    new_name = data.get("name")
    if new_name and new_name != zone.name and repo.get_by_name(new_name):
        raise HTTPException(status.HTTP_409_CONFLICT, "Зона с таким названием уже есть")
    return _to_out(repo.update(zone, data))


@router.delete("/{zone_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_zone(zone_id: int, db: Session = Depends(get_db)):
    repo = ZoneRepository(db)
    repo.delete(_get_or_404(repo, zone_id))
    return Response(status_code=204)
