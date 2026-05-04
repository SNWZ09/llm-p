#импорт репозиторий сообщений и клиент OpenRouter
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient

class ChatUseCase:
    def __init__(self, chat_repo: ChatMessageRepository, llm_client: OpenRouterClient):
        self._chat_repo = chat_repo
        self._llm_client = llm_client
        
    #метод вопроса
    #собираем список сообщений
    #добавляем инструкцию (если есть)
    #получаем историю, добавляем в сообщения
    #и добавляем текущий промпт, как юзер-сообщение
    async def ask(self, user_id: int, prompt: str, system: str | None,
        max_history: int) -> str:
        
        #сюда пишем всё, что должна прочитать нейросеть перед ответом
        messages_for_llm = []
        
        #передаем системную инструкцию на первое место списка
        if system:
            messages_for_llm.append({'role': 'system', 'content': system})
            
        #достаем историю переписки и добавляем в контекст
        #с помощью цикла
        history = await self._chat_repo.get_last_n_messages(user_id = user_id,
            limit = max_history)
        for i in history:
            messages_for_llm.append({'role': i.role, 'content': i.content})
            
        #добавляем текущий запрос
        messages_for_llm.append({'role': 'user', 'content': prompt})
        
        #сохраняем его в БД
        await self._chat_repo.add_message(user_id = user_id, role = 'user', content = prompt)
        
        #на основе всего добавленного в messages_for_llm делаем запрос 
        answer_text = await self._llm_client.ask_model(messages_for_llm)
        
        #сохраняем ответ в БД
        await self._chat_repo.add_message(user_id = user_id, role = 'assistant', content = answer_text)
        
        #выводим ответ
        return answer_text

    #метод запроса истории из репозитория
    async def get_history(self, user_id: int, limit: int = 50):
        return await self._chat_repo.get_last_n_messages(user_id = user_id, limit=limit)
    
    #метод удаления истории пользователя
    async def clear_history(self, user_id: int):
        await self._chat_repo.delete_history(user_id)     
