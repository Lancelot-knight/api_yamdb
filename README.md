### Описание проекта:

Проект YamDB.

YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором

Запросы к API начинаются с /api/v1

---

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/<username>/api_final_yatube.git
```

```
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

---

### Модуль AUTH:

Используется аутентификация с использованием JWT-токенов.

Регистрация нового пользователя POST ```/auth/signup```

Получение JWT-токена в обмен на username и confirmation code POST ```/auth/token```

### Модуль USERS:

Получение списка всех пользователей GET ```/users```

Добавление пользователя POST ```/users/```

Получение пользователя по username GET ```/users/{username}/```

Изменение данных пользователя по username PATCH ```/users/{username}/```

Удаление пользователя по username DELETE ```/users/{username}/```

Получение данных своей учетной записи GET ```/users/me/```

Изменение данных своей учетной записи PATCH ```/users/me/```