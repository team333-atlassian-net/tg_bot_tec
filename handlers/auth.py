"""Хэндлеры для работы с аутенфикацией пользователей"""
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dao.auth import get_user, update_or_add_tg_id
from aiogram.filters import Command


router = Router()

class AuthStates(StatesGroup):
    """Класс состояний для авторизации пользователя по ПИН-коду"""
    awaiting_pin = State()


@router.message(Command("login"))
async def start_handler(message: Message, state: FSMContext):
    """Стартовый хэндлер для авторизации"""
    await message.answer("Здравствуйте! Пожалуйста, введите ваш ПИН-код для авторизации:")
    await state.set_state(AuthStates.awaiting_pin)


@router.message(AuthStates.awaiting_pin)
async def handle_pin(message: Message, state: FSMContext):
    """Ввод пин кода и проверка, что такой юзер есть в системе"""
    pin = message.text.strip()
    tg_id = message.from_user.id

    user = await get_user(pin_code=pin)

    if not user:
        await message.answer("ПИН-код не найден.")
        return

    if user.tg_id and user.tg_id != tg_id:
        await message.answer("Этот ПИН-код уже использован другим пользователем.")
        return

    await update_or_add_tg_id(user, tg_id)

    await message.answer(f"Добро пожаловать, {user.first_name}!")
    await state.clear()
