from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Machine(Base):
    """Станок или 3D-принтер."""

    __tablename__ = "machines"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text, default="")
    image_url: Mapped[str | None] = mapped_column(String(300), default=None)
    # Характеристики в виде словаря: {"Область печати": "220×220×250 мм", ...}
    specs: Mapped[dict] = mapped_column(JSON, default=dict)
    quantity: Mapped[int] = mapped_column(default=1)
    status: Mapped[str] = mapped_column(String(20), default="available")  # available | maintenance
    zone_id: Mapped[int] = mapped_column(ForeignKey("zones.id"))

    zone: Mapped["Zone"] = relationship(back_populates="machines")
