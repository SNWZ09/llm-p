#запрос клиента на базовый URL OpenRouter
#взял httpx из pyproject.toml
import httpx

#импорт настроек и ошибки внешнего сервиса
#'должен собирать заголовки Authorization, 
#HTTP-Referer и X-Title, 
#которые берутся из настроек...
#Если OpenRouter вернул код ошибки,
#клиент должен выбросить доменную ошибку внешнего сервиса'
from app.core.config import settings
from app.core.errors import ExternalServiceError

class OpenRouterClient:
    #метод принимает список словарей сообщений
    #всё это выглядит, как история диалога в формате:
    #роль, контент и тд
    #возвращает только ответ ИИ
    async def ask_model(self, messages: list[dict]) -> str:
    #Клиент должен собирать заголовки, 
    #которые берутся из настроек
        headers = {
            'Authorization': settings.openrouter_api_key,
            'HTTP-Referer': settings.openrouter_site_url,
            'X-Title': settings.openrouter_app_name
        }
        
        #тело запроса
        #(модель и история сообщений)
        payload = {
            'model': 'stepfun/step-3.5-flash:free',
            'messages': messages
        }
        
        #теперь нужно открыть клиент для связи с 'интернетом'
        #так же, на всякий-всякий случай, укажем ещё время 
        #максимального ответа нейросети - 40 секунд
        #(возможно надо будет увеличить)
        #строчку ниже подсмотрел, прошу прощения
        #не понимал, как открыть клиент
        #на платформе async with использовалась только с engine
        async with httpx.AsyncClient() as client: 
            response = await client.post(
            f'{settings.openrouter_base_url}/chat/completions',
            json = payload,
            headers = headers,
            timeout = 40.0
        )
        
        #подсмотрел нужное значение status_code
        if response.status_code != 200:
            print("=== КЛЮЧ ИЗ НАСТРОЕК ===", settings.openrouter_api_key)
            print("=== ОТВЕТ ОТ СЕРВЕРА ===", response.text)
            raise ExternalServiceError(f'Ошибка внешнего сервиса {response.text}')
            
        data = response.json()
        
        return data['choices']['message']['content']
        
        
    
