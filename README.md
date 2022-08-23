# Foodgram - Продуктовый помощник

![example workflow](https://github.com/letulip/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Описание

На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Ключевые функции

- Работа с рецептами (получение, создание, обновление, удаление, добавление в избранное)
- Работа с подписками на авторов (получение, создание, обновление, удаление)
- Работа с пользователями (получение, создание, обновление, удаление)
- Создание, обновление и проверка Djoser токенов пользователей
- Для детального описания функционала API применена библиотека Redoc

## Шаблон .env файла

**Secret** - секрет Джанго
**DB_ENGINE** - движок postgres
**DB_NAME** - имя БД
**POSTGRES_USER** - пользователь БД
**POSTGRES_PASSWORD** - пароль БД
**DB_HOST** - название сервиса (контейнера)
**DB_PORT** - порт для подключения к БД

## Требования

Перед началом установки убедитесь, что на компьютере установлены:

- [Docker](https://docs.docker.com/engine/install/) - может быть установлен через терминал или как десктопное приложение, для большей информации перейдите по ссылке

> Если вы установили Docker Desktop, значит что плагин Docker у вас тоже уже установлен

- [Docker Compose](https://docs.docker.com/compose/install/)

## Установка и запуск проекта

Перед началом установки перейдите на компьютере в директорию в которой дальше будете продолжать работать с проектом используя терминал для Unix систем или командную строку (или любой эмулятор терминала) для Windows.

> Все действия в процессе установки проводятся в терминале для Unix систем или командной строке для Windows.

1. Скачайте проект к себе на компьютер:

  ```bash
  git clone git@github.com:letulip/foodgram-project-react.git
  ```

1. Перейдите в директорию проекта, создайте виртуальное окружение и активируйте его:

  ```bash
  cd foodgram-project-react/
  python3 -m venv venv
  source venv/bin/activate
  ```

1. Перейдите в директорию **backend** и установите необходимые зависимости для проекта:

  ```bash
  cd backend/
  python3 -m pip install -r requirements.txt
  ```

1. Выполните миграции:

  ```bash
  python3 foodgram/manage.py migrate
  ```

1. Перейдите в директорию **infra**

  ```bash
  cd ../infra/
  ```

1. Соберите контейнеры и запустите их:

  ```bash
  docker-compose up -d --build
  ```

1. Выполните по очереди команды:

  ```bash
  docker-compose exec backend python manage.py migrate
  docker-compose exec backend python manage.py dbupload
  docker-compose exec backend python manage.py createsuperuser
  docker-compose exec backend python manage.py collectstatic --no-input
  ```

  > После сборки появится 3 контейнера:
  >
  > 1. контейнер базы данных **db**
  > 2. контейнер приложения **backend**
  > 3. контейнер web-сервера **nginx**
  >

1. Готово! Проект запущен на компьютере и доступен по адресу http://localhost/

## Сайт

Сайт доступен по ссылке: http://yp.letulip.ru

## Авторы

Владимирский Игорь

 > Email: ivladimirskiy@ya.ru
 > Telegram: @letulip
