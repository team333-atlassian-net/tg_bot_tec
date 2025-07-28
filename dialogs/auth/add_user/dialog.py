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
from states import AddUserSG
from dialogs.auth.add_user.handlers import *
from dialogs.auth.add_user.getters import *

logger = logging.getLogger(__name__)


method_window = Window(
    Const("Как вы хотите добавить пользователей?"),
    Row(
        Button(Const("📄 Excel"), id="excel", on_click=on_excel_chosen),
        Button(Const("✍️ Вручную"), id="manual", on_click=on_manual_chosen),
    ),
    Button(
        Const("✍️ Добавить администратора"), id="admin", on_click=on_manual_admin_chosen
    ),
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
    Const(
        "📄 Пришлите Excel-файл (.xlsx) с колонками:\nfirst_name, last_name, middle_name"
    ),
    MessageInput(on_excel_uploaded, content_types=["document"]),
    Row(
        Cancel(Const("❌ Отмена")),
    ),
    state=AddUserSG.upload_excel,
)


dialog = Dialog(
    method_window,
    first_name_window,
    last_name_window,
    middle_name_window,
    confirm_window,
    upload_excel_window,
)
