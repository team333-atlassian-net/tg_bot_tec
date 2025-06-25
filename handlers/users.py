import io
import pandas as pd
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dao.auth import add_user, add_user_with_excel
from aiogram.filters import Command
from models import User
from utils.auth import require_admin
from utils.generate_pin import generate_unique_pin

router = Router()

class AddUserStates(StatesGroup):
    """Класс состояний для добавления нового пользователя в систему (администратором)"""
    choosing_method = State()
    first_name = State()
    last_name = State()
    middle_name = State()
    pin_code = State()
    upload_excel_file = State()


@router.message(Command("add_user"))
async def start_add_user(message: Message, state: FSMContext):
    """Команда для выбора способа добавления пользователец в систему"""
    await require_admin(message) # проверка что админ авторизован
    await message.answer("Как вы хотите добавить пользователей?\n\nВведите <b>вручную</b> или <b>excel</b>")
    await state.set_state(AddUserStates.choosing_method)

########################################################
# Функции для добавления пользователя в систему  вручную
@router.message(AddUserStates.choosing_method, F.text.lower() == "вручную")
async def manual_entry_start(message: Message, state: FSMContext):
    await require_admin(message)
    await message.answer("Введите имя:")
    await state.set_state(AddUserStates.first_name)

@router.message(AddUserStates.first_name)
async def get_first_name(message: Message, state: FSMContext):
    await require_admin(message)
    await state.update_data(first_name=message.text.strip())
    await message.answer("Введите фамилию:")
    await state.set_state(AddUserStates.last_name)

@router.message(AddUserStates.last_name)
async def get_last_name(message: Message, state: FSMContext):
    await require_admin(message)
    await state.update_data(last_name=message.text.strip())
    await message.answer("Введите отчество:")
    await state.set_state(AddUserStates.middle_name)

@router.message(AddUserStates.middle_name)
async def get_middle_name(message: Message, state: FSMContext):
    await require_admin(message)
    await state.update_data(middle_name=message.text.strip())
    
    data = await state.get_data()
    pin_code = await generate_unique_pin()

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        middle_name=data["middle_name"],
        pin_code=pin_code,
        tg_id=None
    )
    await add_user(user)

    await message.answer(f"✅ Пользователь добавлен.\n📌 PIN-код: <b>{pin_code}</b>", parse_mode="HTML")
    await state.clear()

#####################################################################
# Функция для добавления пользователей через excel
@router.message(AddUserStates.choosing_method, F.text.lower() == "excel")
async def excel_entry_start(message: Message, state: FSMContext):
    await require_admin(message)
    await message.answer("Пришлите Excel-файл (.xlsx) с колонками: first_name, last_name, middle_name")
    await state.set_state(AddUserStates.upload_excel_file)


@router.message(AddUserStates.upload_excel_file, F.document)
async def handle_excel(message: Message):
    """Добавление пользователей с помощью файла excel"""
    await require_admin(message)

    file = message.document
    if not file.file_name.endswith(".xlsx"):
        await message.answer("Пожалуйста, отправьте Excel-файл с расширением .xlsx")
        return

    file_bytes = await message.bot.download(file)
    df = pd.read_excel(io.BytesIO(file_bytes.read()))

    required_columns = {"first_name", "last_name", "middle_name"}
    if not required_columns.issubset(df.columns):
        await message.answer("❌ В Excel-файле должны быть колонки: first_name, last_name, middle_name")
        return

    added = await add_user_with_excel(df)

    await message.answer(f"✅ Загружено {added} новых пользователей из Excel.")