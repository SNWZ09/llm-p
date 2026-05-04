#схема запроса к чату и схема ответа
#помимо pydantic есть typing (Optional)
#чтобы предусмотреть поле system 
#как необязательную системную инструкцию

from pydantic import BaseModel, Field
from typing import Optional

#схема запроса к нейросети
class ChatRequest(BaseModel):
    #делааем поле prompt обязательным (...)
    prompt: str = Field(..., description = 'Напишите текст запроса')
    
    #а поле system, наоборот, необязательное
    system: Optional[str] = Field(None, description = 'Системная инструкция')
    
    #'память' нейросети
    max_history: int = Field(10, ge = 0, description = 'Сколько сообщений учитывать')
    
    #креативность
    temperature: float = Field(0.5m ge = 0.0, le = 2.0, description = 'Креативность ответов'

#схема ответа нейросети
#тут просто возвращаем ответ
class ChatResponse(BaseModel):
    answer: str
