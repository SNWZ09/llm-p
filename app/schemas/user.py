#публичная схема пользователя (без пароля и хеша)

from pydantic import BaseModel, EmailStr

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: str
    
    #чтобы FastAPI мог возвращать ORM-объекты напрямую как схему
    model_config = {"from_attributes": True}
