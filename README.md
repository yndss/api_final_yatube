# Проект: API для социальной сети Yatube

## Описание
API даёт возможность приложениям работать с социальной сетью Yatube без прямого доступа к базе. Можно читать и публиковать посты, оставлять комментарии, управлять подписками. Проект построен на Django 3.2, Django REST Framework и использует JWT для авторизации.

## Установка
Чтобы запустить проект локально, выполните шаги:

1. Клонируйте репозиторий и перейдите в папку проекта:

   ```bash
   git clone <URL вашего репозитория>
   cd api_final_yatube
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv venv
   # Windows
   venv\\Scripts\\activate
   # Linux / macOS
   # source venv/bin/activate
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Перейдите в директорию с `manage.py` и примените миграции:

   ```bash
   cd yatube_api
   python manage.py migrate
   ```

5. Создайте суперпользователя при необходимости:

   ```bash
   python manage.py createsuperuser
   ```

6. Запустите сервер разработки:

   ```bash
   python manage.py runserver
   ```

Приложение будет доступно по адресу `http://127.0.0.1:8000/`. База данных по умолчанию хранится в файле `yatube_api/db.sqlite3`.

## Примеры запросов к API
Все маршруты расположены под префиксом `/api/`.

### Получение JWT-токена
`POST /api/jwt/create/`

**Тело запроса**
```json
{
  "username": "user1",
  "password": "password123"
}
```

**Ответ**
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```
Используйте выдаваемый `access`-токен в заголовке `Authorization: Bearer <access_token>`.

### Обновление JWT-токена
`POST /api/jwt/refresh/`

**Тело запроса**
```json
{
  "refresh": "<refresh_token>"
}
```

**Ответ**
```json
{
  "access": "<new_access_token>"
}
```

### Получение списка подписок пользователя
`GET /api/follow/`

**Ответ**
```json
[
  {
    "user": "user1",
    "following": "author_1"
  },
  {
    "user": "user1",
    "following": "author_2"
  }
]
```

### Подписка на автора
`POST /api/follow/`

**Тело запроса**
```json
{
  "following": "author_3"
}
```

**Ответ**
```json
{
  "user": "user1",
  "following": "author_3"
}
```
При попытке подписаться на самого себя вернётся ошибка 400.

### Получение списка постов
`GET /api/posts/`

**Ответ (пример элемента)**
```json
{
  "id": 1,
  "text": "Первый пост",
  "pub_date": "2023-08-01T12:00:00Z",
  "author": "author_1",
  "image": null,
  "group": 2
}
```

### Создание нового поста
`POST /api/posts/`

**Тело запроса**
```json
{
  "text": "Сегодня был в парке",
  "group": 2,
  "image": null
}
```

**Ответ**
```json
{
  "id": 5,
  "text": "Сегодня был в парке",
  "pub_date": "2023-08-02T10:15:00Z",
  "author": "user1",
  "image": null,
  "group": 2
}
```

### Получение комментариев к посту
`GET /api/posts/{post_id}/comments/`

**Ответ (пример элемента)**
```json
{
  "id": 3,
  "text": "Классный пост",
  "author": "commenter",
  "post": 1,
  "created": "2023-08-02T11:30:00Z"
}
```

### Добавление комментария к посту
`POST /api/posts/{post_id}/comments/`

**Тело запроса**
```json
{
  "text": "Поддерживаю!"
}
```

**Ответ**
```json
{
  "id": 4,
  "text": "Поддерживаю!",
  "author": "user1",
  "post": 1,
  "created": "2023-08-02T11:45:00Z"
}
```

## Полезные материалы
- Документация ReDoc доступна по адресу `/redoc/`.
- В папке `postman_collection/` лежит коллекция запросов и скрипт для заполнения тестовыми данными.

## Тесты
Для запуска тестов используйте команду:

```bash
pytest
```

Если при установке возникают ошибки, проверьте версию Python (желательно 3.9+) и убедитесь, что виртуальное окружение активировано.
