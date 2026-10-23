# Machine Catalog

FastAPI + SQLite backend and a small Vue 3 client for a machinery and 3D printer catalog. API docs are generated automatically at `/api/docs` (OpenAPI JSON at `/api/openapi.json`).

## Run locally

cd .\backend
python -m pip install -r requirements.txt
python seed_data.py
python run.py

SQLite database persists in `backend/shop.db`. Cart state is client-owned: requests send `{ "items": [{"product_id": 1, "quantity": 2}] }`. http://localhost:8000/api/docs

## Docker

`docker compose up --build` starts the frontend and API. Open http://localhost. The compose stack uses Nginx as a reverse proxy; API docs are at http://localhost/api/docs. For a public HTTPS deployment, point DNS to your server and configure TLS certificate paths in `nginx/nginx.conf`; the included `deploy.sh` documents the initial host setup but does not issue certificates automatically.

## API overview

- `GET /api/categories`, `GET /api/categories/{id}`
- `GET /api/products?category_id=&skip=0&limit=100`, `GET /api/products/{id}`
- `GET /api/products/category/{id}`
- `POST /api/cart/add`, `GET /api/cart`, `PUT /api/cart/update`, `DELETE /api/cart/remove/{product_id}`
- `GET /health`, `GET /`

For the stateless cart, send the current `items` list in cart add/update requests. Responses include normalized items, total and item count.
