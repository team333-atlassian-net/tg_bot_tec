import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from config import settings
from handlers import canteen

API_TOKEN = settings.API_TOKEN

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
    await message.answer("Привет! Это бот по онбордингу сотрудников компании")


# Регистрируем роутер в диспетчере
dp.include_router(router)
dp.include_router(canteen.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
