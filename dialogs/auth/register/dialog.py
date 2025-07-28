import logging

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Button

from states import RegisterDialogSG
from dialogs.auth.register.handlers import *
from dialogs.auth.register.getters import *

logger = logging.getLogger(__name__)


first_name_window = Window(
    Const("👤 Введите ваше имя:"),
    MessageInput(on_first_entered),
    Cancel(Const("❌ Отмена")),
    state=RegisterDialogSG.first,
)

last_name_window = Window(
    Const("👤 Введите вашу фамилию:"),
    MessageInput(on_last_entered),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=RegisterDialogSG.last,
)

middle_name_window = Window(
    Const("👤 Введите ваше отчество:"),
    MessageInput(on_middle_entered),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=RegisterDialogSG.middle,
)

confirm_window = Window(
    Format(
        "🔎 Подтвердите корректность данных:\n\n"
        "👤 Имя: <b>{first_name}</b>\n"
        "👤 Фамилия: <b>{last_name}</b>\n"
        "👤 Отчество: <b>{middle_name}</b>"
    ),
    Row(
        Button(Const("✅ Подтвердить"), id="confirm_register", on_click=on_confirm),
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=RegisterDialogSG.confirm,
    getter=get_confirm_data,
)

dialog = Dialog(
    first_name_window,
    last_name_window,
    middle_name_window,
    confirm_window,
)
