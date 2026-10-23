from app.routes.categories import router as categories_router
from app.routes.products import router as products_router
from app.routes.cart import router as cart_router

__all__ = ["categories_router", "products_router", "cart_router"]
