from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models import Product


class ProductRepository:
    def get_all(self, db: Session, category_id: int | None = None, skip: int = 0, limit: int = 100) -> tuple[list[Product], int]:
        query = select(Product).options(joinedload(Product.category))
        count_query = select(func.count(Product.id))
        if category_id is not None:
            query = query.where(Product.category_id == category_id)
            count_query = count_query.where(Product.category_id == category_id)
        items = list(db.scalars(query.order_by(Product.id).offset(skip).limit(limit)).unique().all())
        return items, db.scalar(count_query) or 0

    def get_by_id(self, db: Session, product_id: int) -> Product | None:
        return db.scalar(select(Product).options(joinedload(Product.category)).where(Product.id == product_id))

    def get_by_category(self, db: Session, category_id: int) -> list[Product]:
        return list(db.scalars(select(Product).options(joinedload(Product.category)).where(Product.category_id == category_id).order_by(Product.id)).unique().all())

    def create(self, db: Session, **values) -> Product:
        product = Product(**values)
        db.add(product)
        db.commit()
        return self.get_by_id(db, product.id)

    def get_multiple_by_ids(self, db: Session, product_ids: list[int]) -> list[Product]:
        if not product_ids:
            return []
        return list(db.scalars(select(Product).options(joinedload(Product.category)).where(Product.id.in_(product_ids))).unique().all())
