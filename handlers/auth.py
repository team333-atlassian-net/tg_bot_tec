"""Хэндлеры для работы с аутенфикацией пользователей"""
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Router, F
from dao.auth import add_user, create_registration_request, get_request, get_user, get_users, update_or_add_tg_id, update_request_status
from aiogram.filters import Command
from models import User
from utils import generate_pin


router = Router()

class AuthStates(StatesGroup):
    """Класс состояний для авторизации пользователя по ПИН-коду"""
    awaiting_pin = State()

class RegisterRequestStates(StatesGroup):
    """Класс состояний для регистрации пользователя"""
    first_name = State()
    last_name = State()
    middle_name = State()

#######################################################################
# Авторизация пользователя
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
        await message.answer("ПИН-код не найден. Попробуйте заново вызвать login")
        await state.clear()
        return

    if user.tg_id and user.tg_id != tg_id:
        await message.answer("Этот ПИН-код уже использован другим пользователем. Попробуйте заново вызвать login")
        await state.clear()
        return

    await update_or_add_tg_id(user, tg_id)

    await message.answer(f"Добро пожаловать, {user.first_name}!")
    await state.clear()

##########################################################
# Регистрация пользователя

@router.message(Command("register"))
async def register_start(message: Message, state: FSMContext):
    await state.set_state(RegisterRequestStates.first_name)
    await message.answer("Введите ваше имя:")

@router.message(RegisterRequestStates.first_name)
async def enter_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text.strip())
    await state.set_state(RegisterRequestStates.last_name)
    await message.answer("Введите вашу фамилию:")

@router.message(RegisterRequestStates.last_name)
async def enter_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text.strip())
    await state.set_state(RegisterRequestStates.middle_name)
    await message.answer("Введите ваше отчество:")


@router.message(RegisterRequestStates.middle_name)
async def reg_middle_name(message: Message, state: FSMContext):
    data = await state.get_data()
    first_name = data["first_name"]
    last_name = data["last_name"]
    middle_name = message.text.strip()
    tg_id = str(message.from_user.id)

    request = await create_registration_request(tg_id, first_name, last_name, middle_name)
    request_id = request.id

    await message.answer("Заявка на регистрацию отправлена. Ожидайте подтверждения.")
    await state.clear()

    admins = await get_users(admin_rule=True)
    for admin in admins:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Принять", callback_data=f"approve:{request_id}")],
            [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject:{request_id}")]
        ])
        await message.bot.send_message(
            chat_id=admin.tg_id,
            text=f"Новая заявка:\n<b>{last_name} {first_name} {middle_name}</b>",
            reply_markup=kb
        )


@router.callback_query(F.data.startswith("approve:"))
async def approve_request(callback: CallbackQuery):
    request_id = callback.data.split(":")[1]
    request = await get_request(id=request_id)
    pin = generate_pin()

    await update_request_status(request_id=request_id, status="approved")
    user = User(
        tg_id=int(request.tg_id),
        first_name=request.first_name,
        last_name=request.last_name,
        middle_name=request.middle_name,
        pin_code=pin,
        admin_rule=False
    )
    await add_user(user)

    await callback.message.bot.send_message(chat_id=int(request.tg_id), text=f"Ваша заявка одобрена. Ваш ПИН: <b>{pin}</b>")
    await callback.message.answer(
        text=f"👤 Пользователь <b>{request.last_name} {request.first_name}</b> успешно зарегистрирован.\n"
             f"Ему отправлен ПИН-код: <b>{pin}</b>"
    )

    await callback.answer("Пользователь добавлен.")

@router.callback_query(F.data.startswith("reject:"))
async def reject_request(callback: CallbackQuery):
    request_id = callback.data.split(":")[1]
    request = await get_request(id=request_id)
    await update_request_status(request_id=request_id, status="rejected")
    await callback.message.bot.send_message(chat_id=int(request.tg_id), text="Ваша заявка отклонена.")
    await callback.message.answer(
        text=f"Заявка от <b>{request.last_name} {request.first_name}</b> была отклонена."
    )

    await callback.answer("Заявка отклонена.")