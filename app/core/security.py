#импорты для работы с временем
#используем их, чтобы задать срок годности для токена
#timezone используем, чтобы 'унифицировать' время его создания
#timedelta используем для вычисления разницы во времени
from datetime import datetime, timedelta, timezone

#импорт для хэширования пароля
from passlib.context import CryptContext

#импорт для работы с jwt-токенами
from jose import jwt

#импорт для подключения созданных ранее настроек
from app.core.config import settings

#используем алгоритм bcrypt
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    #функция берет обычный пароль и превращает его
    #в 'непонятную' строку
    return pwd_context.hash(password)
    
def verify_password(password: str, hashed_password: str) -> bool:
    #функция проверяет, что введённый пароль 
    #соответствует сохранённому хэшу
    return pwd_context.verify(password, hashed_password)
    
def create_access_token(user_id: int, role: str) -> str:
    #вычисляем, когда токен истечёт
    #для этого берем текущее время и прибавляем к нему
    #количество минут, указанных в настройках
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    #запоминаем время выдачи токена
    iat = datetime.now(timezone.utc)
    
    #создаем payload, чтобы связать его с токеном
    payload = {
        'sub': str(user_id), #владелец токена
        'role': role, #роли владельца токена
        'exp': expire, #время, когда токен перестанет работать
        'iat': iat #время, когда токен был создан
    }

    #с помощью jwt.encode подписываем наш payload
    #секретным ключом с помощью алгоритма 
    #(всё берётся из config.py
    #и получаем итоговый токен
    return jwt.encode(payload, settings.jwt_secret, algorithm = settings.jwt_alg)
    
#теперь осталось создать функцию декодирования токена
#используем те же данные, что и в jwt.encode
#в settings.jwt_alg используем квадратные скобки
#потому что без них у меня не сработало...
#не знаю почему, честно.. Прошу прощения
def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithm = [settings.jwt_alg])
