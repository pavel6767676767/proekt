#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
if [ ! -f backend/.env ]; then
  cp backend/.env.example backend/.env
  echo "Created backend/.env. Review settings before deploying."
fi
docker compose up -d --build
echo "Catalog is running. Configure HTTPS at your host proxy or update nginx/nginx.conf with certificate paths."
