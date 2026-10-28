from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "5 этаж: мастерские школы"
    debug: bool = False
    database_url: str = "sqlite:///./floor5.db"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # Токен для изменения данных (POST/PUT/DELETE). Обязательно поменяй в .env
    admin_token: str = "change-me"

    # Общая информация о 5 этаже (отдаётся на /api/about)
    floor_title: str = "5 этаж"
    floor_description: str = "Школьные мастерские: станки, 3D-принтеры и всё для проектов."
    floor_hours: str = ""
    floor_contact: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
