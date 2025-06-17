import io
import pandas as pd
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dao.auth import add_user, add_user_with_excel, get_user, update_or_add_tg_id
from aiogram.filters import Command
from models import User

router = Router()

class AuthStates(StatesGroup):
    awaiting_pin = State()

class AddUserStates(StatesGroup):
    choosing_method = State()
    first_name = State()
    last_name = State()
    middle_name = State()
    pin_code = State()


async def is_admin(tg_id: int) -> bool:
    """Функция, проверяющая, что роль - админ"""
    user = await get_user(tg_id=tg_id, admin_rule=True)
    return user is not None


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


@router.message(Command("add_user"))
async def start_add_user(message: Message, state: FSMContext):
    """Команда для выбора способа добавления пользователец в систему"""
    if not await is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора.")
        return

    await message.answer("Как вы хотите добавить пользователей?\n\nВведите <b>вручную</b> или <b>excel</b>")
    await state.set_state(AddUserStates.choosing_method)

########################################################
# Функции для добавления пользователя в систему  вручную
@router.message(AddUserStates.choosing_method, F.text.lower() == "вручную")
async def manual_entry_start(message: Message, state: FSMContext):
    await message.answer("Введите имя:")
    await state.set_state(AddUserStates.first_name)

@router.message(AddUserStates.first_name)
async def get_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text.strip())
    await message.answer("Введите фамилию:")
    await state.set_state(AddUserStates.last_name)

@router.message(AddUserStates.last_name)
async def get_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text.strip())
    await message.answer("Введите отчество:")
    await state.set_state(AddUserStates.middle_name)

@router.message(AddUserStates.middle_name)
async def get_middle_name(message: Message, state: FSMContext):
    await state.update_data(middle_name=message.text.strip())
    await message.answer("Введите ПИН-код:")
    await state.set_state(AddUserStates.pin_code)

@router.message(AddUserStates.pin_code)
async def get_pin_code(message: Message, state: FSMContext):
    pin_code = message.text.strip()
    data = await state.get_data()

    user = await get_user(pin_code=pin_code)
    if user:
        await message.answer("❌ Пользователь с таким  ПИН-кодом уже существует. Попробуйте другой.")
        return

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        middle_name=data["middle_name"],
        pin_code=pin_code,
        tg_id=None
    )
    await add_user(user)
    await message.answer("✅ Пользователь добавлен.")
    await state.clear()

#####################################################################

# Функция для добавления пользователей через excel

@router.message(AddUserStates.choosing_method, F.text.lower() == "excel")
async def excel_entry_start(message: Message):
    await message.answer("Пришлите Excel-файл (.xlsx) с колонками: first_name, last_name, middle_name, pin_code")

@router.message(F.document)
async def handle_excel(message: Message):
    if not await is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора.")
        return

    file = message.document
    if not file.file_name.endswith(".xlsx"):
        await message.answer("Пожалуйста, отправьте Excel-файл с расширением .xlsx")
        return

    file_bytes = await message.bot.download(file)
    df = pd.read_excel(io.BytesIO(file_bytes.read()))

    required_columns = {"first_name", "last_name", "middle_name", "pin_code"}
    if not required_columns.issubset(df.columns):
        await message.answer("❌ В Excel-файле должны быть колонки: first_name, last_name, middle_name, pin_code")
        return

    added = await add_user_with_excel(df)

    await message.answer(f"✅ Загружено {added} новых пользователей из Excel.")