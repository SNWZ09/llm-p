#импорт usecases, созданных схем, ошибок
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError

#HTTP-эндпоинты
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

#создаем роутер с тегом auth
router = APIRouter(prefix='/auth', tags=['auth'])

#эндпоинт регистрации
#клиент получит только публичные данные
@router.post('/register', response_model=UserPublic)
async def register(data: RegisterRequest,
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)):
    
    #передаем логику регистрации
    #статусы подсмотрел
    try:
        return await auth_usecase.register(data.email, data.password)
    
    #если эл. адрес занят
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
  
#эндпоинт логина 
@router.post('/login', response_model=TokenResponse)
async def login(

    #'Эндпоинт логина должен работать в формате OAuth2 для Swagger,
    #то есть принимать OAuth2PasswordRequestForm,
    #использовать username как email и возвращать TokenResponse'
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)
):
    try:
        token = await auth_usecase.login(form_data.username, form_data.password)
        return TokenResponse(access_token=token)
        
    #если неверный паролл
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        
#эндпоинт получения профиля
@router.get('/me', response_model=UserPublic)
async def get_me(
    #нужно, чтобы пользователь был авторизован
    user_id: int = Depends(get_current_user_id),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase)
):
    try:
        return await auth_usecase.get_profile(user_id)
    
    #профиль не найден
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        
        
