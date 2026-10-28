"""Заполняет базу ПРИМЕРАМИ. Замени данные на реальные станки 5 этажа.

Запуск из папки backend:  python -m app.seed
"""
from app.database import SessionLocal, init_db
from app.models import Machine, Zone

DATA = {
    "3D-печать": {
        "description": "Печатаем прототипы и детали для проектов.",
        "machines": [
            {
                "name": "3D-принтер (пример)",
                "description": "Замени на реальную модель.",
                "specs": {"Технология": "FDM", "Материалы": "PLA, PETG"},
                "quantity": 2,
            },
        ],
    },
    "Лазерная резка": {
        "description": "Резка и гравировка фанеры, акрила, картона.",
        "machines": [
            {
                "name": "Лазерный станок (пример)",
                "description": "Замени на реальную модель.",
                "specs": {"Материалы": "фанера, акрил"},
            },
        ],
    },
}


def run() -> None:
    init_db()
    with SessionLocal() as db:
        if db.query(Zone).first():
            print("В базе уже есть данные, ничего не добавляю.")
            return
        for zone_name, zone_data in DATA.items():
            zone = Zone(name=zone_name, description=zone_data["description"])
            zone.machines = [Machine(**m) for m in zone_data["machines"]]
            db.add(zone)
        db.commit()
        print("Готово: примеры добавлены.")


if __name__ == "__main__":
    run()
