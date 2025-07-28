import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.mongo import MongoStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.types import Message
from aiogram_dialog import setup_dialogs
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from dialogs import get_dialogs
from handlers.start import router as start_router
from handlers.add_user import router as add_users_router
from handlers.canteen import router as canteen_router
from handlers.company_info import router as company_info_router
from handlers.events import router as events_router
from handlers.faq import router as faq_router
from handlers.feedback import router as feedback_router
from handlers.guides import router as guides_router
from handlers.login import router as login_router
from handlers.organizational_structure import router as org_structure_router
from handlers.register import router as register_router
from handlers.request_register_callbacks import router as register_request_router
from handlers.virtual_excursions import router as virtual_excursion_router
from utils.auth import require_auth

# configure_logging()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

bot = Bot(
    token=settings.API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
mongo_storage = MongoStorage(
    client=AsyncIOMotorClient("mongodb://root:example@localhost:27017"),
    key_builder=DefaultKeyBuilder(with_destiny=True),
)
dp = Dispatcher(
    storage=mongo_storage,
)

dp.include_router(start_router)
# dp.include_router(login_router)
# dp.include_router(register_router)
# dp.include_router(register_request_router)
# dp.include_router(add_users_router)
# dp.include_router(events_router)
# dp.include_router(company_info_router)
# dp.include_router(virtual_excursion_router)
# dp.include_router(org_structure_router)
# dp.include_router(faq_router)
# dp.include_router(canteen_router)
# dp.include_router(guides_router)
# dp.include_router(feedback_router)

dp.include_routers(*get_dialogs())
setup_dialogs(dp)

#
# @dp.message(Command("start"))
# async def start_handler(message: Message):
#     """Стартовый хэндлер"""
#     await message.answer(
#         "Привет! Это бот для онбординга сотрудников компании ТЭК.\nЧтобы увидеть все команды, введите /help"
#     )
#
#
# @dp.message(Command("help"))
# async def help_handler(message: Message):
#     """Хэндлер со справочной информацией"""
#
#     user = await require_auth(message)  # проверка, что пользователь авторизован
#     if not user:
#         return
#
#     if user.admin_rule:  # Команды для администратора
#         help_text = (
#             "📌 <b>Доступные команды для администратора:</b>\n\n"
#             "/add_user — Добавить пользователя(ей) вручную или через файл Excel\n"
#             "/add_event — Добавить и разослать информацию о мероприятии\n"
#             "/manage_events — Управление корпоративными мероприятиями\n"
#             "/add_company_info — Добавить информацию о компании\n"
#             "/manage_company_info — Управление информацией о компании\n"
#             "/add_virtual_excursion — Создать виртуальную экскурсию\n"
#             "/add_excursion_material — Добавить материалы экскурсии\n"
#             "/manage_virtual_excursions — Управление виртуальными экскурсиями\n"
#             "/add_org_structure — Добавить информацию об организационной структуре\n"
#             "/manage_org_structures — Управление организационной структурой\n"
#             "/add_faq — Добавить вопрос и ответ\n"
#             "/manage_faq — Управление часто задаваемыми вопросами\n"
#             "/add_canteen_info — Добавить информацию по столовой или меню\n"
#             "/add_guide — Добавить инструкцию по оформлению документа\n"
#             "/manage_guides — Управление инструкциями по оформлению документов\n"
#             "/manage_feedback — Управление обратной связью\n\n"
#             "📌 <b>Общие команды:</b>\n\n"
#             "/start — Начать взаимодействие с ботом\n"
#             "/login — Авторизация по ПИН-коду\n"
#             "/register — Регистрация в системе\n"
#             "/help — Показать это справочное сообщение\n"
#             "/events — Показать список всех корпоративных мероприятий\n"
#             "/company_info — Показать информацию о компании\n"
#             "/virtual_excursions — Показать список виртуальных экскурсий\n"
#             "/org_structures — Показать организационную структуру\n"
#             "/faq — Показать часто задаваемые вопросы\n"
#             "/search_faq — Поиск по вопросам\n"
#             "/canteen — Показать информацию по столовой или меню\n"
#             "/guides — Показать инструкции по оформлению документов\n"
#             "/feedback — Обратная связь\n"
#         )
#     else:  # Команды для обычного пользователя
#         help_text = (
#             "📌 <b>Доступные команды:</b>\n\n"
#             "/start — Начать взаимодействие с ботом\n"
#             "/login — Авторизация по ПИН-коду\n"
#             "/register — Регистрация в системе\n"
#             "/help — Показать это справочное сообщение\n"
#             "/events — Показать список всех корпоративных мероприятий\n"
#             "/company_info — Показать информацию о компании\n"
#             "/virtual_excursions — Показать список виртуальных экскурсий\n"
#             "/org_structures — Показать организационную структуру\n"
#             "/faq — Показать часто задаваемые вопросы\n"
#             "/search_faq — Поиск по вопросам\n"
#             "/canteen — Показать информацию по столовой или меню\n"
#             "/guides — Показать инструкции по оформлению документов\n"
#             "/feedback — Обратная связь\n"
#         )
#
#     await message.answer(help_text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
