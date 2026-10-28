from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import MachineRepository, ZoneRepository
from app.schemas import MachineCreate, MachineOut, MachineUpdate
from app.security import require_admin

router = APIRouter(prefix="/api/machines", tags=["Станки и принтеры"])


def _get_or_404(repo: MachineRepository, machine_id: int):
    machine = repo.get(machine_id)
    if machine is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Станок не найден")
    return machine


def _check_zone(db: Session, zone_id: int) -> None:
    if ZoneRepository(db).get(zone_id) is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Такой зоны не существует")


@router.get("", response_model=list[MachineOut])
def list_machines(
    zone_id: int | None = None,
    machine_status: Literal["available", "maintenance"] | None = Query(default=None, alias="status"),
    search: str | None = None,
    db: Session = Depends(get_db),
):
    return MachineRepository(db).list(zone_id=zone_id, status=machine_status, search=search)


@router.get("/{machine_id}", response_model=MachineOut)
def get_machine(machine_id: int, db: Session = Depends(get_db)):
    return _get_or_404(MachineRepository(db), machine_id)


@router.post("", response_model=MachineOut, status_code=201, dependencies=[Depends(require_admin)])
def create_machine(payload: MachineCreate, db: Session = Depends(get_db)):
    _check_zone(db, payload.zone_id)
    return MachineRepository(db).create(payload.model_dump())


@router.put("/{machine_id}", response_model=MachineOut, dependencies=[Depends(require_admin)])
def update_machine(machine_id: int, payload: MachineUpdate, db: Session = Depends(get_db)):
    repo = MachineRepository(db)
    machine = _get_or_404(repo, machine_id)
    data = payload.model_dump(exclude_unset=True)
    if "zone_id" in data:
        _check_zone(db, data["zone_id"])
    return repo.update(machine, data)


@router.delete("/{machine_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_machine(machine_id: int, db: Session = Depends(get_db)):
    repo = MachineRepository(db)
    repo.delete(_get_or_404(repo, machine_id))
    return Response(status_code=204)
