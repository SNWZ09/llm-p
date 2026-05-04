#здесь опишем ORM-модели.
#Пользователь с полями: id, email, password_hash,
#role, created_at.
#модель сообщения чата ChatMessage с полями:
#id, user_id, role, content, created_at.

from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class User(Base):
    __tablename__ = 'users'
    
    #опишем столбцы таблицы
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    
    #в роли решил написать дефолтное значение, т.к., мне кажется,
    #что это важно предусмотреть
    role: Mapped[str] = mapped_column(String, default='user')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    #настройка  связи relationship 
    #между пользователем и сообщениями
    #cascade отвечает за поведение при удалении
    #и при работе с дочерними объектами. 
    #cascade=“all, delete-orphan” означает: 
    #если вы удаляете user, его сообщения
    #удалятся вместе с ним. И если вы удалили 
    #сообщение из списка так, 
    #что оно осталось “сиротой”, 
    #оно тоже удалится.
    #(взято из урока на платформе)
    messages: Mapped[list['ChatMessage']] =  relationship(back_populates='ChatMessage', cascade='all, delete-orphan')
    
#теперь опишем сообщения чата
class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    #опишем внешний ключ user_id
    user_id: Mapped[int] = mapped_column(ForeignKey('user_id'), nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    
    #текст сообщения и время его создания
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # связь 'каждое сообщение принадлежит только одному пользователю'
    user: Mapped['User'] = relationship('User', back_populates='messages')
