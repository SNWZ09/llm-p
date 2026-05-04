#импорт, тк нам понадобится создание SQL-запросов
from sqlalchemy import select, delete

#импорт для асинхронного подключения к БД
from sqlalchemy.ext.asyncio import AsyncSession

#импорт ORM-модели сообщения
from app.db.models import ChatMessage

class UserRepository:
    #'Репозиторий должен принимать AsyncSession
    #в конструктор и хранить его как приватное поле.'
    def __init__(self, session: AsyncSession):
        self._session = session
        
    #метод сохранения сообщения (роли и контента)
    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        message = ChatMessage(user_id = user_id, role = role, content = content)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message
    
    #метод получения последних ... сообщений пользователя
    #с сортировкой
    async def get_last_n_messages(self, user_id: int, limit: int) -> list[ChatMessage]:
        statement = (
            select(ChatMessage).where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc()).limit(limit)
        )
        
        #получаем список и выгружаем его (scalars().all()))
        result = await self._session.execute(statement)
        messages = list(result.scalars().all())
        
        #ставим -1, чтобы порядок был
        #'от самого старого к самому новому'
        return messages[::-1]
        
    #метод удаления истории
    #не очень понял по условию, должно ли после этого
    #что-то возвращаться, поэтому напишу None
    async def delete_history(self, user_id: int) -> None:
        statement = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self._session.commit()
        await self._session.refresh(statement)
