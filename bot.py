import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from config import settings
from handlers import users
from utils.auth import require_auth

API_TOKEN = settings.API_TOKEN

# Создаём основные объекты
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

router = Router()

@router.message(Command('start'))
async def start_handler(message: Message):
    """Стартовый хэндлер"""
    await message.answer("Привет! Это бот для онбординга сотрудников компании ТЭК.\nЧтобы увидеть все команды, введите /help")

@router.message(Command("help"))
async def help_handler(message: Message):
    """Хэндлер со справочной информацией"""
    
    user = await require_auth(message) # проверка что пользователь авторизован
    
    if user.admin_rule: # команды для админа
        help_text = (
            "📌 <b>Доступные команды для администратора:</b>\n\n"
            "/add_user - Добавить пользователя(ей) в систему вручную или с помощью файла Excel\n"
            "📌 <b>Общедоступные команды:</b>\n\n"
            "/start — Начать взаимодействие с ботом\n"
            "/login — Авторизация по ПИН-коду\n"
            "/register - Регистрация в системе\n"
            "/help — Показать это справочное сообщение\n"
        )
    else: # команды для обычного пользователя
        help_text = (
            "📌 <b>Доступные команды:</b>\n\n"
            "/start — Начать взаимодействие с ботом\n"
            "/login — Авторизация по ПИН-коду\n"
            "/register - Регистрация в системе\n"
            "/help — Показать это справочное сообщение\n"
        )
    await message.answer(help_text)


dp.include_router(router)
dp.include_router(users.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
