from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self):
        self.repo = ProductRepository()
        self.categories = CategoryRepository()

    def list_products(self, db: Session, category_id: int | None, skip: int, limit: int):
        return self.repo.get_all(db, category_id, skip, limit)

    def get_product(self, db: Session, product_id: int):
        product = self.repo.get_by_id(db, product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def get_category_products(self, db: Session, category_id: int):
        if self.categories.get_by_id(db, category_id) is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return self.repo.get_by_category(db, category_id)

    def create_product(self, db: Session, values: dict):
        if self.categories.get_by_id(db, values["category_id"]) is None:
            raise HTTPException(status_code=400, detail="Category does not exist")
        return self.repo.create(db, **values)
