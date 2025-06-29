from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.bot import DefaultBotProperties

from config import settings
from utils.auth import require_auth
from dialogs import register_all_dialogs
from handlers.login import router as login_router
from handlers.register import router as register_router
from handlers.request_register_callbacks import router as register_request_router
from handlers.add_user import router as add_users_router
from handlers.events import router as events_router

bot = Bot(token=settings.API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

register_all_dialogs(dp)

dp.include_router(login_router)
dp.include_router(register_router)
dp.include_router(register_request_router)
dp.include_router(add_users_router)
dp.include_router(events_router)

@dp.message(Command('start'))
async def start_handler(message: Message):
    """Стартовый хэндлер"""
    await message.answer("Привет! Это бот для онбординга сотрудников компании ТЭК.\nЧтобы увидеть все команды, введите /help")

@dp.message(Command("help"))
async def help_handler(message: Message):
    """Хэндлер со справочной информацией"""
    
    user = await require_auth(message) # проверка что пользователь авторизован
    if not user:
        return
    
    if user.admin_rule: # команды для админа
        help_text = (
            "📌 <b>Доступные команды для администратора:</b>\n\n"
            "/add_user - Добавить пользователя(ей) в систему вручную или с помощью файла Excel\n"
            "/add_event - Добавить и разослать информацию о новом корпоротивном мероприятии\n"
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
            "/events - Показать список всех корпоративных мероприятий\n"
            "/help — Показать это справочное сообщение\n"
        )
    await message.answer(help_text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())