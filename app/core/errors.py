#файл, в котором указаны собственные исключения приложения
#'Должны быть базовая ошибка приложения и типовые наследники: 
#конфликт (например, email уже существует), 
#неавторизован (неверный пароль), запрещено (нет прав), 
#не найдено (объект в базе отсутствует), 
#ошибка внешнего сервиса (например, OpenRouter вернул ошибку)'

class AppError(Exception)
    'Базовая ошибка приложения'
    pass
    
class ConflictError(AppError)
    'Произошел конфликт данных'
    pass
    
class UnauthorizedError(AppError)
    'Ошибка аутентификации'
    pass
    
class ForbiddenError(AppError)
    'Недостаточно прав'
    pass
    
class NotFoundError(AppError)
    'Объект отсутствует в базе данных'
    pass
    
class ExternalServiceError(AppError)
    'Ошибка внешнего сервиса'
    pass
