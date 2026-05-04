#импорт функций, которые создают
#и предоставляют сессию базы данных,
#репозитории и usecase-объекты через Depends
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.db.session import AsyncSessionLocal
from app.core.config import settings
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase

#сначала сделаем кнопку авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

#метод создания и закрытия сессии
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
        
#методы получения репозиториев (пользователей,
#чатов, клиента OpenRouter)
#используем просто def, тк нет сетевых запросов

def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)

def get_chat_repo(session: AsyncSession = Depends(get_session)) -> ChatMessageRepository:
    return ChatMessageRepository(session)

def get_llm_client() -> OpenRouterClient:
    return OpenRouterClient()
    
#методы получения usecase-объектов
def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repo)) -> AuthUseCase:
    return AuthUseCase(user_repo)

def get_chat_usecase(
    chat_repo: ChatMessageRepository = Depends(get_chat_repo),
    llm_client: OpenRouterClient = Depends(get_llm_client)) -> ChatUseCase:
    return ChatUseCase(chat_repo, llm_client)
    
#метод проверки jwt-токена и извлечение id юзера из sub
#Прошу прощения, подсмотрел, было очень сложно разобраться
#с этой проверкой
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось проверить данные',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
        user_id_str: str = payload.get('sub')
        if user_id_str is None:
            raise credentials_exception
        return int(user_id_str)
        
    #если токен просрочился - выкидываем ошибку
    except JWTError:
        raise credentials_exception
        

