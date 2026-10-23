from pydantic import BaseModel, Field

from app.schemas.product import ProductResponse


class CartItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class CartItemUpdate(CartItemCreate):
    pass


class CartRequest(BaseModel):
    items: list[CartItemCreate] = Field(default_factory=list)


class CartItem(BaseModel):
    product: ProductResponse
    quantity: int
    subtotal: float


class CartResponse(BaseModel):
    items: list[CartItem]
    total: float
    items_count: int
