# API smoke checks

Start API: `python run.py`. Browse Swagger at `http://localhost:8000/api/docs`.

```sh
curl http://localhost:8000/health
curl http://localhost:8000/api/categories
curl 'http://localhost:8000/api/products?category_id=1'
curl http://localhost:8000/api/products/1
curl -X POST http://localhost:8000/api/cart/add -H 'Content-Type: application/json' -d '{"product_id":1,"quantity":2,"items":[]}'
curl -X PUT http://localhost:8000/api/cart/update -H 'Content-Type: application/json' -d '{"product_id":1,"quantity":1,"items":[{"product_id":1,"quantity":2}]}'
curl -X POST http://localhost:8000/api/cart/remove/1 -H 'Content-Type: application/json' -d '{"items":[{"product_id":1,"quantity":1}]}'
```

Cart endpoints are stateless: send the complete client-side cart in `items` on each request. The delete endpoint also accepts the current cart as repeated JSON query values, so clients may instead update their local cart and send its new content to `GET /api/cart`.
