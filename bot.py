import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from config import settings
from dao.auth import get_user
from handlers import canteen, auth, users

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
    await message.answer("Привет! Это бот для онбординга сотрудников компании ТЭК.\n Чтобы увидеть все команды, введите /help")

@router.message(Command("help"))
async def help_handler(message: Message):
    """Хэндлер со справочной информацией"""

    tg_id = message.from_user.id
    user = await get_user(tg_id=tg_id)

    if not user: # проверка что пользователь авторизован
        await message.answer("Вы не авторизованы. Введите пин-код с помощью /login.\n Для регистрации введите /register")
        return
    
    if user.admin_rule: # команды для админа
        help_text = (
            "📌 <b>Доступные команды для администратора:</b>\n\n"
            "/start — Начать взаимодействие с ботом\n"
            "/login — Авторизация по ПИН-коду\n"
            "/help — Показать это справочное сообщение\n"
            "/add_user - Добавить пользователя(ей) в систему вручную или с помощью файла excel\n"
            "столовая — Информация о работе столовой\n"
        )
    else: # команды для обычного пользователя
        help_text = (
            "📌 <b>Доступные команды:</b>\n\n"
            "/start — Начать взаимодействие с ботом\n"
            "/login — Авторизация по ПИН-коду\n"
            "/help — Показать это справочное сообщение\n"
            "столовая — Информация о работе столовой\n"
        )
    await message.answer(help_text)


dp.include_router(router)
dp.include_router(canteen.router)
dp.include_router(auth.router)
dp.include_router(users.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
