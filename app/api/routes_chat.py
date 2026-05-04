#HTTP-эндпоинты
from fastapi import APIRouter, Depends, HTTPException, status

#импорт usecases, созданных схем, ошибок
from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase
from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError

#создаем роутер с тегом chat
router = APIRouter(prefix='/chat', tags=['chat'])

#эндпоинт /chat
#принимаем вопрос, проверяем токен
@router.post("", response_model=ChatResponse)
async def ask_chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase)
):

    #отдаём все данные usecase, получаем ответ
    try:
        answer = await chat_usecase.ask(
            user_id=user_id,
            prompt=request.prompt,
            system=request.system,
            max_history=request.max_history
        )
        return ChatResponse(answer=answer)
        
    #если произошла ошибка на стороне OpenRouter 
    except ExternalServiceError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

#эндпоинт получения истории через usecase,
#который возвращает список сообщений
@router.get('/history')
async def get_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase)
):
    #достаём историю и выводим
    messages = await chat_usecase.get_history(user_id=user_id)
    return {'items': messages}

#эндпоинт с методом DELETE,
#который очищает историю
@router.delete('/history')
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase)
):
    #удаляем историю сообщений
    await chat_usecase.clear_history(user_id=user_id)
    return {'status': 'История очищена'}
