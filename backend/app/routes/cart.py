from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.cart import CartRequest, CartResponse
from app.services.cart_service import CartService

router = APIRouter(prefix="/api/cart", tags=["cart"])
service = CartService()


@router.get("", response_model=CartResponse)
def get_cart(db: Session = Depends(get_db)):
    return service.get_cart_details(db, [])


@router.post("/add", response_model=CartResponse)
def add_to_cart(payload: CartRequest, db: Session = Depends(get_db)):
    return service.get_cart_details(db, [item.model_dump() for item in payload.items])


@router.put("/update", response_model=CartResponse)
def update_cart(payload: CartRequest, db: Session = Depends(get_db)):
    return service.get_cart_details(db, [item.model_dump() for item in payload.items])


@router.post("/remove/{product_id}", response_model=CartResponse)
def remove_from_cart(product_id: int, payload: CartRequest, db: Session = Depends(get_db)):
    items = [item.model_dump() for item in payload.items if item.product_id != product_id]
    return service.get_cart_details(db, items)
