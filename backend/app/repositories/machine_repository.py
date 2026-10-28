from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Machine


class MachineRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        zone_id: int | None = None,
        status: str | None = None,
        search: str | None = None,
    ) -> list[Machine]:
        query = select(Machine).order_by(Machine.name)
        if zone_id is not None:
            query = query.where(Machine.zone_id == zone_id)
        if status is not None:
            query = query.where(Machine.status == status)
        if search:
            query = query.where(Machine.name.ilike(f"%{search}%"))
        return list(self.db.scalars(query))

    def get(self, machine_id: int) -> Machine | None:
        return self.db.get(Machine, machine_id)

    def create(self, data: dict) -> Machine:
        machine = Machine(**data)
        self.db.add(machine)
        self.db.commit()
        self.db.refresh(machine)
        return machine

    def update(self, machine: Machine, data: dict) -> Machine:
        for key, value in data.items():
            setattr(machine, key, value)
        self.db.commit()
        self.db.refresh(machine)
        return machine

    def delete(self, machine: Machine) -> None:
        self.db.delete(machine)
        self.db.commit()
