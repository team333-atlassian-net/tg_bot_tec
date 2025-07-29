# tg_bot_tec

## Клонируйте репозиторий
```
git clone https://github.com/team333-atlassian-net/tg_bot_tec.git
cd tg_bot_tec
```
## Активация виртуального окружения
В командной строке ввести:
```
python -m venv venv
```
```
venv\Scripts\activate.bat 
```
или для linux/mac

```
source venv/bin/activate 
```
## Установка зависимостей

```
pip install -r requirements.txt
```

## Переменные окружения
(корень проекта) - создать файл .env

```
API_TOKEN="8050664861:AAFDbw9lAcEU_0zzreICgBSEUxhFW-kj-hE"
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/onboarding_chat
```

!!! В postgres должна быть создана БД

## Запуск docker-compose

```
docker compose up -d
```

## Миграции

В командной строке ввести:
```bash
alembic upgrade head
```

## Заполнение БД
Запустить скрипты:
```
python -m create_scripts.create_users
```
```
python -m create_scripts.create_mock_data
```

## Запуск бота

```
python bot.py
```

Ссылка на бота: [TestTECBot](https://t.me/test_tec_bot)
