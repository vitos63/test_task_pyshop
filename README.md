## Описание проекта

Данное REST API является тестовым заданием на позицию Python Developer(trainee) 

## Установка


1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/vitos63/test_task_pyshop.git
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    venv\Scripts\activate 
    ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

## Запуск

Запустите сервер redis:

```bash
sudo service redis-server start
```

Перейдите в папку test_task_pyshop:

```bash
cd test_task_pyshop
```

Создайте и примините миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

Запустите тестовый веб-сервер:

```bash
python manage.py runserver
```

# 📌 API Авторизации и Аутентификации

## 📂 Маршруты API

### 1️⃣ Регистрация пользователя  
**POST** `/api/register/`  
Создает нового пользователя.

#### 🔹 Пример запроса и ответа:
```
Endpoint: `/api/register/`
Method: `POST
Body: `{"username": "testuser", "email": "user@example.com", "password": "password"}`
Response: `{"id": 1, "username": "testuser", "email": "user@example.com"}`
```

### 2️⃣ Вход в систему  
**POST** `/api/login/`  
Позволяет пользователю войти в систему и получить access и refresh токены.  

#### 🔹 Пример запроса и ответа:
```
Endpoint: `/api/login/`
Method: `POST
Body: `{"email": "user@example.com", "password": "password"}`
Response: `{"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsImV4cCI6MTcxMjE0NTk0NiwiaWF0IjoxNzEyMTQ1OTE2fQ.KX6LM66tC3p3bUCdkWRQkPvariP8tzUfWd8Z13akCPY", "refresh_token": "d952527b-caef-452c-8c93-1100214f82e5"}`
```

### 3️⃣ Обновление токенов  
**POST** `/api/refresh/`  
Обновляет access_token и refresh_token, используя refresh_token.

#### 🔹 Пример запроса и ответа:
```
Endpoint: `/api/refresh/`
Method: `POST
Body: `{"refresh_token": "d952527b-caef-452c-8c93-1100214f82e5"}`
Response: `{"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiZXhhbXBsZVVzZXIiLCJleHAiOjE3MTIxNDYxNDd9.zKobBlRuOiJSxCmi-iYap1bejfnvK6M3qtnkT0ssDKA", "refresh_token": "eb0464c2-ed6e-4346-a709-042c33946154"}`
```

### 4️⃣ Выход из системы  
**POST** `/api/logout/`  
Пользователь выходит из системы, у него удаляется refresh_token.

#### 🔹 Пример запроса и ответа:
```
Endpoint: `/api/logout/`
Method: `POST
Body: `{"refresh_token": "eb0464c2-ed6e-4346-a709-042c33946154"}`
Response: `{"success": "User logged out."}`
```

### 5️⃣ Получение профиля пользователя  
**GET** `/api/me/`  
Возвращает информацию о текущем пользователе.

#### 🔹 Пример запроса и ответа:
```
Endpoint: `/api/me/`
Method: `GET
Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiZXhhbXBsZVVzZXIiLCJleHAiOjE3MTIxNDYxNDd9.zKobBlRuOiJSxCmi-iYap1bejfnvK6M3qtnkT0ssDKA
Response: `{"id": 1, "username": "testuser", "email": "user@example.com"}`
```

### 6️⃣ Изменение личной информации пользователя
**PUT** `/api/me/`  
Изменяет информацию пользователя и возвращает ее в ответе.

#### 🔹 Пример запроса и ответа:
```
Endpoint: `/api/me/`
Method: `PUT
Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiZXhhbXBsZVVzZXIiLCJleHAiOjE3MTIxNDYxNDd9.zKobBlRuOiJSxCmi-iYap1bejfnvK6M3qtnkT0ssDKA
Body: {"username": "John Smith"}
Response: `{"id": 1, "username": "John Smith", "email": "user@example.com"}`
```