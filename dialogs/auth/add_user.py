import logging
import io
import pandas as pd

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Row

from dao.auth import add_user, add_user_with_excel
from models import User
from utils.generate_pin import generate_unique_pin
from utils.auth import require_admin

logger = logging.getLogger(__name__)


class AddUserSG(StatesGroup):
    method = State()
    first_name = State()
    last_name = State()
    middle_name = State()
    confirm = State()
    upload_excel = State()


# --- Обработчики ручного ввода ---

async def on_manual_chosen(callback: CallbackQuery, button, manager: DialogManager):
    manager.dialog_data["is_admin"] = False
    await manager.switch_to(AddUserSG.first_name)

async def on_manual_admin_chosen(callback: CallbackQuery, button, manager: DialogManager):
    manager.dialog_data["is_admin"] = True
    await manager.switch_to(AddUserSG.first_name)


async def on_first_name_entered(message: Message, widget: TextInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["first_name"] = message.text
    await dialog_manager.switch_to(AddUserSG.last_name)

async def on_last_name_entered(message: Message, widget: TextInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["last_name"] = message.text
    await dialog_manager.switch_to(AddUserSG.middle_name)

async def on_middle_name_entered(message: Message, widget: TextInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["middle_name"] = message.text
    await dialog_manager.switch_to(AddUserSG.confirm)

async def get_manual_confirm_data(dialog_manager: DialogManager, **kwargs):
    return {
        "dialog_data": {
            "first_name": dialog_manager.dialog_data.get("first_name"),
            "last_name": dialog_manager.dialog_data.get("last_name"),
            "middle_name": dialog_manager.dialog_data.get("middle_name"),
        }
    }

async def on_manual_confirm(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data
    pin = await generate_unique_pin()
    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        middle_name=data["middle_name"],
        pin_code=pin,
        tg_id=None,
        admin_rule=data.get("is_admin", False),
    )
    await add_user(user)
    status = "администратор" if user.admin_rule else "пользователь"
    await callback.message.answer(f"✅ {status.capitalize()} добавлен.\n📌 PIN-код: <b>{pin}</b>")
    logger.info("Администратор зарегистрировал пользователя вручную (/add_user)")
    await dialog_manager.done()

# --- Обработчики Excel ---

async def on_excel_chosen(callback: CallbackQuery, button, manager: DialogManager):
    await manager.switch_to(AddUserSG.upload_excel)

async def on_excel_uploaded(message: Message, widget, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return

    file = message.document
    if not file.file_name.endswith(".xlsx"):
        await message.answer("❌ Пожалуйста, отправьте Excel-файл с расширением .xlsx")
        return

    file_bytes = await message.bot.download(file)
    df = pd.read_excel(io.BytesIO(file_bytes.read()))
    required_columns = {"first_name", "last_name", "middle_name"}

    if not required_columns.issubset(df.columns):
        await message.answer("❌ В Excel-файле должны быть колонки: first_name, last_name, middle_name")
        return

    added_users = await add_user_with_excel(df)
    if added_users:
        pin_messages = "\n".join(
            [f"🔐 Пин-код для пользователя <b>{full_name}</b>: <code>{pin}</code>" for full_name, pin in added_users]
        )
        await message.answer(
            f"✅ Загружено {len(added_users)} пользователей.\n\n{pin_messages}\n\n📌 Передайте PIN-коды пользователям."
        )
    else:
        await message.answer("⚠️ Ни один пользователь не был добавлен.")
    logger.info("Администратор зарегистрировал пользователей с помощью Excel (/add_user)")
    await dialog_manager.done()


# --- Окна ---

method_window = Window(
    Const("Как вы хотите добавить пользователей?"),
    Row(
        Button(Const("📄 Excel"), id="excel", on_click=on_excel_chosen),
        Button(Const("✍️ Вручную"), id="manual", on_click=on_manual_chosen),
    ),
    Button(Const("✍️ Добавить администратора"), id="admin", on_click=on_manual_admin_chosen),
    Cancel(Const("❌ Отмена")),
    state=AddUserSG.method,
)

first_name_window = Window(
    Const("Введите имя пользователя:"),
    MessageInput(on_first_name_entered),
    Cancel(Const("❌ Отмена")),
    state=AddUserSG.first_name,
)

last_name_window = Window(
    Const("Введите фамилию пользователя:"),
    MessageInput(on_last_name_entered),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=AddUserSG.last_name,
)

middle_name_window = Window(
    Const("Введите отчество пользователя:"),
    MessageInput(on_middle_name_entered),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=AddUserSG.middle_name,
)

confirm_window = Window(
    Format(
        "Подтвердите добавление пользователя:\n\n"
        "👤 Имя: {dialog_data[first_name]}\n"
        "👤 Фамилия: {dialog_data[last_name]}\n"
        "👤 Отчество: {dialog_data[middle_name]}"
    ),
    Row(
        Button(Const("✅ Сохранить"), id="confirm", on_click=on_manual_confirm),
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=AddUserSG.confirm,
    getter=get_manual_confirm_data,
)

upload_excel_window = Window(
    Const("📄 Пришлите Excel-файл (.xlsx) с колонками:\nfirst_name, last_name, middle_name"),
    MessageInput(on_excel_uploaded, content_types=["document"]),
    Row(
        Cancel(Const("❌ Отмена")),
    ),
    state=AddUserSG.upload_excel,
)


add_user_dialog = Dialog(
    method_window,
    first_name_window,
    last_name_window,
    middle_name_window,
    confirm_window,
    upload_excel_window,
)
