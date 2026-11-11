# Быстрая проверка API

Запустите `python run.py` и в другом терминале проверьте:

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/api/about
Invoke-RestMethod http://localhost:8000/api/zones
Invoke-RestMethod http://localhost:8000/api/machines
Invoke-RestMethod 'http://localhost:8000/api/machines?search=3D'
```

Для управления каталогом передавайте HTTP Basic Auth с логином и паролем из `backend/.env`. Например, в Postman выберите Authorization → Basic Auth. Проверка данных входа: `POST http://localhost:8000/api/admin/login` с JSON `{"username":"...","password":"..."}`. Все операции изменения каталога требуют тот же Basic Auth.
