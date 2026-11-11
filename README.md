# EduTech: оборудование для учебных мастерских

Сайт на Vue показывает учебное оборудование из API. Backend полностью написан на Python: FastAPI, SQLAlchemy и SQLite. Страница из `proekt.html` перенесена в Vue и теперь загружает данные из базы; зоны соответствуют категориям, станки — позициям каталога. API-документация: `/api/docs`.

## Запуск всего проекта одной командой (рекомендуется)

Установите и запустите Docker Desktop. Откройте PowerShell в корне `proekt-main` и выполните:

```powershell
docker compose up --build -d
```

Docker сам соберёт и запустит backend, frontend и Nginx вместе. Сайт откроется на `http://localhost`, админка — `http://localhost/admin`, API — `http://localhost/api/docs`. Остановить всё можно командой `docker compose down`.

Этот способ не требует отдельно запускать `python run.py` и `npm.cmd run dev`. Инструкции ниже для локальной разработки, если нужно вручную менять и перезапускать backend или frontend.

## Локальный запуск backend (Windows PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Откройте `backend/.env` и задайте `ADMIN_USERNAME` и `ADMIN_PASSWORD`. Затем запустите:

```powershell
.\.venv\Scripts\python.exe seed_data.py
.\.venv\Scripts\python.exe run.py
```

API будет на `http://localhost:8000`, документация — `http://localhost:8000/api/docs`. Примеры запуска в `backend/test_commands.md`.

## Локальный запуск frontend

Оставьте backend работать и откройте **второй** терминал. Из текущей папки `backend` перейдите во frontend и запускайте через `npm.cmd`: в Windows PowerShell команда `npm` может блокироваться политикой выполнения скриптов.

```powershell
cd ..\frontend
npm.cmd install
npm.cmd run dev
```

Откройте адрес, который покажет Vite (по умолчанию `http://localhost:5173`). Если браузер откроет пустую страницу, сначала запустите backend.

## Админ-панель

Откройте `/admin` и войдите по логину и паролю из `backend/.env`. На этой машине уже создан локальный `.env` с указанными вами данными входа; `.env` исключён из Git. Администратор может добавлять, редактировать и удалять позиции, добавлять разделы и печатать QR-коды, ведущие на карточки оборудования. Каталог перечитывает данные примерно каждые 15 секунд. Характеристики редактируются обычным JSON-объектом, например `{"Технология":"FDM","Область печати":"220×220×250 мм"}`.

## API

- `GET /api/about` — название, описание и сводка.
- `GET /api/zones`, `GET /api/zones/{id}` — разделы каталога.
- `POST /api/zones`, `PUT /api/zones/{id}`, `DELETE /api/zones/{id}` — разделы (нужна Basic Auth).
- `GET /api/machines?zone_id=&status=&search=` и `GET /api/machines/{id}` — оборудование.
- `POST /api/machines`, `PUT /api/machines/{id}`, `DELETE /api/machines/{id}` — оборудование (нужна Basic Auth).
- `POST /api/admin/login` — проверка логина и пароля.

## Docker

Для локального запуска контейнеров создайте `backend/.env` по примеру, укажите логин и пароль, затем из корня выполните `docker compose up --build -d`. Сайт откроется на `http://localhost`; API — на `http://localhost/api/docs`. Для публикации на Ubuntu сервере укажите A-запись домена на IP сервера, откройте порты 80/443 и запустите `chmod +x deploy.sh && ./deploy.sh`. Скрипт спросит логин, пароль (ввод скрыт) и email Let’s Encrypt, после чего включит HTTPS. База SQLite сохраняется в Docker volume. Сертификат можно продлить командой, которую скрипт напечатает после установки.
