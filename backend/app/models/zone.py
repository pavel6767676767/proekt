from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Zone(Base):
    """Зона / мастерская на этаже: 3D-печать, лазерная резка, ЧПУ и т.д."""

    __tablename__ = "zones"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")

    machines: Mapped[list["Machine"]] = relationship(
        back_populates="zone", cascade="all, delete-orphan", order_by="Machine.name"
    )
