from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def list_categories(self, db: Session):
        return self.repo.get_all(db)

    def get_category(self, db: Session, category_id: int):
        category = self.repo.get_by_id(db, category_id)
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
