from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Zone


class ZoneRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Zone]:
        return list(self.db.scalars(select(Zone).order_by(Zone.name)))

    def get(self, zone_id: int) -> Zone | None:
        return self.db.get(Zone, zone_id)

    def get_by_name(self, name: str) -> Zone | None:
        return self.db.scalar(select(Zone).where(Zone.name == name))

    def create(self, data: dict) -> Zone:
        zone = Zone(**data)
        self.db.add(zone)
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def update(self, zone: Zone, data: dict) -> Zone:
        for key, value in data.items():
            setattr(zone, key, value)
        self.db.commit()
        self.db.refresh(zone)
        return zone

    def delete(self, zone: Zone) -> None:
        self.db.delete(zone)
        self.db.commit()
