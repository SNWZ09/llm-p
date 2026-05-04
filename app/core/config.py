#пишем импорты для автоматического считывания переменных из .env
from pydantic_settings import BaseSettings, SettingsConfigDict

#класс для управления настройками приложения 
class Settings(BaseSettings):
    app_name: str
    env: str

    jwt_secret: str
    jwt_alg: str
    access_token_expire_minutes: int

    sqlite_path: str

    openrouter_api_key: str
    openrouter_base_url: str
    openrouter_model: str
    openrouter_site_url: str
    openrouter_app_name: str
    
    #указываем, что переменные нужно читать из файла .env
    #добавил игнор, тк не получал ответа от нейросети
    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8',
        extra='ignore' # Игнорируем лишние переменные, если они есть
    )
    
settings = Settings()
