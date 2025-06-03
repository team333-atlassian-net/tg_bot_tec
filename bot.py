import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from config import settings

API_TOKEN = settings.API_TOKE

# Создаём основные объекты
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# Создаём роутер и регистрируем хендлер
router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Это бот по онбордингу сотрудников компании ТЭК!")

# Регистрируем роутер в диспетчере
dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
