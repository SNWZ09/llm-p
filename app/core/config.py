#пишем импорты для автоматического считывания переменных из .env
from pydantic_settings import BaseSettings, SettingsConfigDict

#класс для управления настройками приложения 
class Settings(BaseSettings):
    APP_NAME: str
    ENV: str

    JWT_SECRET: str
    JWT_ALG: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SQLITE_PATH: str

    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    OPENROUTER_MODEL: str
    OPENROUTER_SITE_URL: str
    OPENROUTER_APP_NAME: str
    
    #указываем, что переменные нужно читать из файла .env
    model_config = SettingsConfigDict(env_file = '.env', env_file_encoding = 'utf-8')
    
settings = Settings()
