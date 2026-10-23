from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category


class CategoryRepository:
    def get_all(self, db: Session) -> list[Category]:
        return list(db.scalars(select(Category).order_by(Category.name)).all())

    def get_by_id(self, db: Session, category_id: int) -> Category | None:
        return db.get(Category, category_id)

    def get_by_slug(self, db: Session, slug: str) -> Category | None:
        return db.scalar(select(Category).where(Category.slug == slug))

    def create(self, db: Session, name: str, slug: str) -> Category:
        category = Category(name=name, slug=slug)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
