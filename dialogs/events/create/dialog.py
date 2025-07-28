import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Button

from states import EventCreationSG
from dialogs.events.create.handlers import *

logger = logging.getLogger(__name__)


title_window = Window(
    Const("Введите название мероприятия:"),
    MessageInput(on_title_input),
    Cancel(Const("❌ Отмена")),
    state=EventCreationSG.title,
)

description_window = Window(
    Const("Введите описание мероприятия:"),
    MessageInput(on_description_input),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=EventCreationSG.description,
)

confirm_window = Window(
    Format(
        "Подтвердите создание мероприятия:\n\nНазвание: {dialog_data[title]}\nОписание: {dialog_data[description]}"
    ),
    Row(
        Button(Const("✅ Сохранить"), id="confirm", on_click=on_confirm_press),
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=EventCreationSG.confirm,
)

dialog = Dialog(title_window, description_window, confirm_window)
