#импорт middleware
#'Middleware существует для того, 
#чтобы вся эта общая логика выполнялась один раз
#для всех запросов, в одном месте, вне бизнес-логики'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#импорт роутеров, настроек, engine и прочего
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

#у роутеров одинаковое название, поэтому идентифицируем их
from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router

#собираем приложение
def create_app() -> FastAPI:
    
    #название берем из настроек
    app = FastAPI(title=settings.app_name)
    
    #настроим взаимодействие браузера с API
    #подсмотрел у нейросети, тк было сложно
    #разобраться где ставить звездочки,
    #куда добавлять CORSMiddleware
    #и прочее.
    #Прошу прощения
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    
    #подключаем роутеры (вход, регистрация, чат)
    app.include_router(auth_router)
    app.include_router(chat_router)
    
    #событие запуска
    @app.on_event('startup')
    async def startup_event():
        #с запуском будут созданы все таблицы
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    #событие выключения        
    @app.on_event('shutdown')
    async def shutdown_event():
        await engine.dispose()
    
    #эндпоинт, который возвращает статус и окружение
    #для быстрой проверки сервера
    @app.get('/health', tags=['health'])
    async def health_check():
        return {'status': 'ok', 'environment': settings.env}

    return app
    
app = create_app()
