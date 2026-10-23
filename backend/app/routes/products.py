from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import ProductCreate, ProductListResponse, ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/api/products", tags=["products"])
service = ProductService()


@router.get("", response_model=ProductListResponse)
def list_products(category_id: int | None = None, skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: Session = Depends(get_db)):
    items, total = service.list_products(db, category_id, skip, limit)
    return {"items": items, "total": total}


@router.get("/category/{category_id}", response_model=list[ProductResponse])
def list_category_products(category_id: int, db: Session = Depends(get_db)):
    return service.get_category_products(db, category_id)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return service.get_product(db, product_id)


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return service.create_product(db, payload.model_dump())
