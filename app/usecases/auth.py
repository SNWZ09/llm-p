#импорт репозитория пользователей, ошибок,
#паролей, а так же пользователей
from app.repositories.users import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.db.models import User

class AuthUseCase:
    #сначала передаём репозиторий
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo
    
    #метод регистрации нового юзера
    #делаем проверку на уникальность эл. адреса
    #хэшируем пароль, всё сохраняем
    async def register(self, email: str, password: str) -> User:
        #если не сложно, напишите в ревью, пожалуйста
        #можно ли эту проверку было сделать в if?
        #или конструкция не позволяет и обязательно нужно сначала
        #присвоить эту проверку переменной existing_user?
        existing_user = await self.user_repo.get_by_email(email)
        if existing user:
            raise ConflictError('Пользователь с таким email уже зарегистрирован')
        
        hashed_pswd = hash_password(password)
        return await self._user_repo.create(email, hashed_pswd)
        
    #метод логина существующего юзера
    async def login(self, email: str, password: str) -> str:
        #ищем по эл. адресу
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError('Неверный email или пароль')
        
        #проверяем пароль и возвращаем токен
        if not verify_password(password, user.password_hash):
            raise UnauthorizedError('Неверный email или пароль')
            
        return create_access_token(user_id = user.id, role = user.role
        
    #метод получения профиля по user_id
    async def get_profile(self, user_id:int) -> User:
        user = await self.user_repo.get_by_id(user_id)
        
        #если не нашелся - выкидываем ошибку
        if not user:
            raise NotFoundError('Пользователь не найден')
            
        return user
    
    
        
