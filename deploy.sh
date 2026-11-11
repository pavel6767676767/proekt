#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"

domain=${DOMAIN:-proekt.s1474.online}
case "$domain" in
  *[!A-Za-z0-9.-]*|.*|*.) echo "Invalid domain name." >&2; exit 1 ;;
esac
if [ ! -f backend/.env ]; then
  cp backend/.env.example backend/.env
fi
chmod 600 backend/.env
if ! grep -q '^ADMIN_PASSWORD=.' backend/.env; then
  printf 'Admin login [moderator1474]: '
  read -r admin_username
  admin_username=${admin_username:-moderator1474}
  printf 'Admin password (input hidden): '
  stty -echo
  read -r admin_password
  stty echo
  printf '\n'
  if [ -z "$admin_password" ]; then
    echo "Admin password cannot be empty." >&2
    exit 1
  fi
  ADMIN_USERNAME_VALUE="$admin_username" ADMIN_PASSWORD_VALUE="$admin_password" python3 - <<'PY'
import os
from pathlib import Path

path = Path("backend/.env")
values = {"ADMIN_USERNAME": os.environ["ADMIN_USERNAME_VALUE"], "ADMIN_PASSWORD": os.environ["ADMIN_PASSWORD_VALUE"]}
lines = [line for line in path.read_text(encoding="utf-8").splitlines() if not line.startswith(tuple(f"{key}=" for key in values))]
lines.extend(f"{key}={value}" for key, value in values.items())
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
  unset admin_password
fi

printf 'Email for Let’s Encrypt certificate notices: '
read -r email
if [ -z "$email" ]; then
  echo "An email address is required for certificate registration." >&2
  exit 1
fi

cp nginx/nginx-http.conf nginx/nginx.conf
docker compose up -d --build
docker compose --profile certbot run --rm certbot certonly \
  --webroot --webroot-path /var/www/certbot \
  --domain "$domain" --email "$email" --agree-tos --no-eff-email --non-interactive --keep-until-expiring

sed "s/__DOMAIN__/${domain}/g" nginx/nginx-https.conf > nginx/nginx.conf
docker compose up -d nginx
echo "HTTPS site deployed: https://${domain}"
echo "Admin panel: https://${domain}/admin"
echo "To renew later: docker compose --profile certbot run --rm certbot renew && docker compose exec -T nginx nginx -s reload"
