from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.product_repository import ProductRepository


class CartService:
    def __init__(self):
        self.products = ProductRepository()

    def get_cart_details(self, db: Session, items: list[dict]):
        quantities: dict[int, int] = {}
        for item in items:
            pid, quantity = int(item["product_id"]), int(item["quantity"])
            if quantity <= 0:
                raise HTTPException(status_code=422, detail="Quantity must be greater than zero")
            quantities[pid] = quantities.get(pid, 0) + quantity
        products = self.products.get_multiple_by_ids(db, list(quantities))
        by_id = {p.id: p for p in products}
        missing = set(quantities) - set(by_id)
        if missing:
            raise HTTPException(status_code=404, detail=f"Products not found: {sorted(missing)}")
        cart_items = [{"product": by_id[pid], "quantity": qty, "subtotal": round(by_id[pid].price * qty, 2)} for pid, qty in quantities.items()]
        return {"items": cart_items, "total": round(sum(x["subtotal"] for x in cart_items), 2), "items_count": sum(quantities.values())}
