### Photo Bank
Фотоальбомы пользователей

#### Описание

Пример работы с фотографиями через CRUD API используя Django Rest Framework

#### Возможности

- Загрузка фото на сервер
- Получение списка фото
- Редактирование названия фото
- Счетчик просмотров фото 
- Регистрация пользователей через логин и пароль
- Авторизация пользователя по токену
- Автосоздание миниатюр на сервере в формате webp
- Создание видео-слайдшоу из 10 лучших фото сайта/юзера по запросу
- Уведомления юзера по почте раз в день о том, что его фото попало в топ-3 лучших фото сайта.

#### Перед запуском проекта:
Создать и активировать виртуальное окружение в папке venv проекта.

Заполнение базы данных:
- `python manage.py init`

Запуск задачи ежедневной отправки писем юзерам о попадании их фото в топ-3 просмотров по сайту:
- `python manage.py run_huey`

#### Пути

- API: `api/v1/`
- Документация: `docs/`
- Админка: `admin/`  логин/пароль: admin/admin
- Видео-слайдшоу:
  - топ 10 фото сайта по просмотрам: `slider/site/`
  - топ 10 фото юзера по просмотрам: `slider/user/<id>`

#### Требования

Необходимо наличие файла `ffmpeg.exe` в папке виртуального окружения проекта `venv/Scripts`

Для Windows качать [здесь](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z):
`https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z`
