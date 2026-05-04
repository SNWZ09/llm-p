# llm-p
Проект по построению защищённого API для работы с большой языковой моделью

1. Установка и запуск проекта через uv
 pip install uv
 uv init 
 uv venv
 source .venv/bin/activate # MacOS/Linux
 .venv\Scripts\activate.bat # Windows
 
 2.Установить зависимости проекта
     [project]
    name = "llm-p"
    version = "0.1.0"
    description = "FastAPI service with JWT auth, SQLite, and OpenRouter LLM proxy"
    requires-python = ">=3.11"
    dependencies = [
      "fastapi>=0.112.0",
      "uvicorn[standard]>=0.30.0",
      "sqlalchemy>=2.0.30",
      "aiosqlite>=0.20.0",
      "pydantic[email]>=2.7.0",
      "pydantic-settings>=2.3.0",
      "python-jose[cryptography]>=3.3.0",
      "passlib[bcrypt]>=1.7.4",
      "httpx>=0.27.0",
      "python-multipart>=0.0.9",
      "greenlet>=3.3.1",
      "bcrypt==4.3.0",
      "ruff>=0.14.14",
    ]
    
    [tool.uv]
    dev-dependencies = []
    uv pip install -r <(uv pip compile pyproject.toml)

3. Требуется получить API-ключ на платформе OpenRouter и вставить его в файл .env в строку OPENROUTER_API_KEY=
4. Пишем настройки проекта (app/core/config.py)
5. Доменные ошибки (app/core/errors.py)
6. Безопасность и токены (app/core/security.py)
7. Инфраструктура базы данных (app/db/session.py)
8. Базовый класс для моделей (app/db/base.py)
9. Описание таблиц: Пользователи и Сообщения (app/db/models.py)
10. Схемы для авторизации (app/schemas/auth.py)
11. Схема профиля пользователя (app/schemas/user.py)
12. Схемы для работы с нейросетью (app/schemas/chat.py)
13. Репозиторий пользователей (app/repositories/users.py)
14. Репозиторий сообщений чата (app/repositories/chat_messages.py)
15. Клиент для OpenRouter (app/services/openrouter_client.py)
16. Бизнес-логика авторизации (app/usecases/auth.py)
17. Бизнес-логика чата (app/usecases/chat.py)
18. Механизм зависимостей (app/api/deps.py)
19. Эндпоинты авторизации (app/api/routes_auth.py)
20. Эндпоинты чата (app/api/routes_chat.py)
21. Собрать всё в app/main.py

Проверить всё линтером (ruff check). Затем перейти к тестам введя (uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000)

Итак, теперь самое интересное. У меня было несколько ошибок в db/models.py, который были успешно исправлены.
 
### 1. Регистрация пользователя
![Регистрация пользователя](https://github.com/SNWZ09/llm-p/blob/5c5799e2a0d53faa300b216ba35b58ce64b84ee4/screenshots/1%20%D0%A0%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F.png)

На этом фото видна успешная регистрация пользователя с 
email: zaremba@example.com
password: string123
Так я успешно зарегистрировался.
Понимаю, что эл. адрес не приведен к стандарту "student_surname@email.com".
Сделал это осознанно, так как дальше у меня возникли проблемы, с которыми я пытался справиться именно на этом аккаунте. Заранее прошу прощения, если так делать было нельзя, и нужно было всё-таки переделать эл. адрес.

### 2. Логин пользователя
![Логин пользователя](https://github.com/SNWZ09/llm-p/blob/01cf2999cae824a26559ef5bf7f7c0f057102616/screenshots/2%20%D0%9B%D0%BE%D0%B3%D0%B8%D0%BD.png)
Тут тоже все нормально. Ввели юзернейм, пароль и снизу получили токен.

### 3. Авторизация пользователя
![Авторизация пользователя 1](https://github.com/SNWZ09/llm-p/blob/main/screenshots/3%20%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F.png?raw=true)
![Авторизация пользователя 2](https://github.com/SNWZ09/llm-p/blob/01cf2999cae824a26559ef5bf7f7c0f057102616/screenshots/4%20%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F.png)

На этих фото видна успешная авторизация с помощью токена, юзернейма и пароля.

### 4. Запрос пользователя
![Запрос пользователя](https://github.com/SNWZ09/llm-p/blob/01cf2999cae824a26559ef5bf7f7c0f057102616/screenshots/5%20%D0%97%D0%B0%D0%BF%D1%80%D0%BE%D1%81.png)

Дальше самое грустное. Сколько бы я ни пытался починить эту ошибку - ничего не помогало. Трижды менял API-ключ. Пять раз менял модели. Дошло до того, что я без ссылки на settings писал напрямую в коде модель и свой ключ. Ничего не помогло.

### 5. История запросов пользователя
![История запросов пользователя](https://github.com/SNWZ09/llm-p/blob/01cf2999cae824a26559ef5bf7f7c0f057102616/screenshots/6%20%D0%98%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F%20%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B9.png)

На скрине видна малая часть всех моих попыток заставить подключение к нейросети работать.
Ниже я напишу все свои запросы-попытки исправить ситуацию.  ID соответствует тому, что был указан при авторизации.

{
  "items": [
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T18:51:02",
      "id": 1,
      "content": "Скажи 20 раз слово МИФИ"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T18:55:09",
      "id": 2,
      "content": "Привет"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T18:56:44",
      "id": 3,
      "content": "Привет"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T18:59:47",
      "id": 4,
      "content": "Привет"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T19:00:05",
      "id": 5,
      "content": "Привет"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T19:01:35",
      "id": 6,
      "content": "string"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T19:05:07",
      "id": 7,
      "content": "string"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T19:09:02",
      "id": 8,
      "content": "string"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T19:12:03",
      "id": 9,
      "content": "string"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T19:12:08",
      "id": 10,
      "content": "string"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T19:15:37",
      "id": 11,
      "content": "stadaddsaring"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T19:18:04",
      "id": 12,
      "content": "asdads"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T19:20:02",
      "id": 13,
      "content": "HI!"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T19:22:22",
      "id": 14,
      "content": "Hi!"
    },
    {
      "user_id": 1,
      "role": "user",
      "created_at": "2026-05-04T19:30:05",
      "id": 15,
      "content": "Привет"
    }
  ]
}


### 6. Удаление истории запросов пользователя
![Удаление истории запросов пользователя 1](https://github.com/SNWZ09/llm-p/blob/01cf2999cae824a26559ef5bf7f7c0f057102616/screenshots/7%20%D0%98%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F%20%D1%83%D0%B4%D0%B0%D0%BB%D0%B5%D0%BD%D0%B0.png)
![Удаление истории запросов пользователя 2](https://github.com/SNWZ09/llm-p/blob/01cf2999cae824a26559ef5bf7f7c0f057102616/screenshots/8%20%D0%98%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F%20%D1%83%D0%B4%D0%B0%D0%BB%D0%B5%D0%BD%D0%B0.png)

Тут видна работоспособность функции удаления истории. Сначала получен успешный ответ. Потом следует проверка get_history, в которой ничего нет.

Если я где-то каким-то образом в коде забыл удалить свой API-ключ, это будет вообще фантастика...
Заранее спасибо за проверку. Извините, что так поздно кидаю работу.
