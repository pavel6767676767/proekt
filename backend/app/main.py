from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routes import cart_router, categories_router, products_router

app = FastAPI(title=settings.app_name, debug=settings.debug, docs_url="/api/docs", openapi_url="/api/openapi.json")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory="static", check_dir=False), name="static")
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(cart_router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Machine Catalog API", "docs": "/api/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
