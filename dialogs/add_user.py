import io
import logging
import pandas as pd
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram.types import Message

from dao.auth import add_user, add_user_with_excel
from models import User
from utils.auth import require_admin
from utils.generate_pin import generate_unique_pin

logger = logging.getLogger(__name__)

class AddUserSG(StatesGroup):
    """Класс сотояния загрузки пользователя"""
    method = State()
    first = State()
    last = State()
    middle = State()
    upload = State()

    
# --- Обработчики переходов ---
async def on_manual_chosen(callback, button, manager: DialogManager):
    await manager.switch_to(AddUserSG.first)

async def on_excel_chosen(callback, button, manager: DialogManager):
    await manager.switch_to(AddUserSG.upload)

async def on_excel_uploaded(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    """Обработка Excel-файла для добавления пользователей"""
    user = await require_admin(message)
    if not user:
        return

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
    logger.info("Администратор зарегистрировал пользователей с помощью excel (/add_user)")
    await dialog_manager.done()

async def on_first_entered(message: Message,
                           value: str,
                           dialog_manager: DialogManager,
                           widget):
    """Обработчик имени"""
    dialog_manager.dialog_data["first_name"] = value.get_value()
    await dialog_manager.switch_to(AddUserSG.last)

async def on_last_entered(message: Message,
                           value: str,
                           dialog_manager: DialogManager,
                           widget):
    """Обработчик фамилии"""
    dialog_manager.dialog_data["last_name"] = value.get_value()
    await dialog_manager.switch_to(AddUserSG.middle)

async def on_middle_entered(message: Message,
                           value: str,
                           dialog_manager: DialogManager,
                           widget):
    """Обработчик отчества
    Регистраирует пользователя"""
    data = dialog_manager.dialog_data
    middle_name = value.get_value()
    pin = await generate_unique_pin()

    user = User(first_name=data["first_name"],
                last_name=data["last_name"],
                middle_name=middle_name,
                pin_code=pin,
                tg_id=None)
    await add_user(user)

    await message.answer(f"✅ Пользователь добавлен.\n📌 PIN-код: <b>{pin}</b>")
    logger.info("Администратор зарегистрировал пользователя вручную (/add_user)")
    await dialog_manager.done()

add_user_dialog = Dialog(
    # Выбор метода
    Window(
        Const("Как вы хотите добавить пользователей?"),
        Row(
            Button(Const("📄 Excel"), id="excel", on_click=on_excel_chosen),
            Button(Const("✍️ Вручную"), id="manual", on_click=on_manual_chosen),
        ),
        state=AddUserSG.method,
    ),
    # Ввод имени
    Window(
        Const("Введите имя:"),
        TextInput(id="first_name", on_success=on_first_entered),
        state=AddUserSG.first,
    ),
    # Ввод фамилии
    Window(
        Const("Введите фамилию:"),
        TextInput(id="last_name", on_success=on_last_entered),
        state=AddUserSG.last,
    ),
    # Ввод отчества
    Window(
        Const("Введите отчество:"),
        TextInput(id="middle_name", on_success=on_middle_entered),
        state=AddUserSG.middle,
    ),
    # Загрузка Excel
    Window(
        Const("Пришлите Excel-файл (.xlsx) с колонками: first_name, last_name, middle_name"),
        MessageInput(on_excel_uploaded, content_types=['document']),
        state=AddUserSG.upload,
    ),
)
