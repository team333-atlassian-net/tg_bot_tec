import logging

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Button

from states import OrgStructureCreationSG
from dialogs.org_structure.create.handlers import *
from dialogs.org_structure.create.getters import *

logger = logging.getLogger(__name__)


title_window = Window(
    Const("Введите название организационной структуры:"),
    MessageInput(on_title_input),
    Cancel(Const("❌ Отмена")),
    state=OrgStructureCreationSG.title,
)

description_window = Window(
    Const("Введите описание (необязательно):"),
    MessageInput(on_description_input),
    Row(
        Back(Const("⬅️ Назад")),
        Button(Const("➡️ Пропустить"), id="skip_desc", on_click=on_description_skip),
        Cancel(Const("❌ Отмена")),
    ),
    state=OrgStructureCreationSG.description,
)

file_window = Window(
    Const("Отправьте файл (необязательно):"),
    MessageInput(on_file_input),
    Row(
        Back(Const("⬅️ Назад")),
        Button(Const("➡️ Пропустить"), id="skip_file", on_click=on_file_skip),
        Cancel(Const("❌ Отмена")),
    ),
    state=OrgStructureCreationSG.file,
)


confirm_window = Window(
    Format(
        "Подтвердите создание информации об организационной структуре:\n\n"
        "Название: {dialog_data[title]}\n"
        "Описание: {dialog_data[description]}\n"
        "Файл: {dialog_data[file_text]}"
    ),
    Row(
        Button(Const("✅ Сохранить"), id="confirm", on_click=on_confirm_press),
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=OrgStructureCreationSG.confirm,
    getter=get_confirm_data,
)

dialog = Dialog(
    title_window,
    description_window,
    file_window,
    confirm_window,
)
