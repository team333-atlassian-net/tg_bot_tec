from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Next,
    Cancel,
    Row,
    Select,
    ScrollingGroup,
    Button,
    Group,
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram.enums import ContentType
from states import FeedbackUserSG
from dialogs.feedback.user.handlers import *


feedback_text_window = Window(
    Const("Расскажите нам о работе бота 😊\n\n"),
    TextInput(id="feedback_input", on_success=on_text_input),
    Cancel(Const("❌ Отмена")),
    state=FeedbackUserSG.text,
)


feedback_attachment_window = Window(
    Const(
        "Можете добавить несколько вложений (только изображения), отправляя их по одному"
    ),
    MessageInput(on_attachment_upload, content_types=[ContentType.PHOTO]),
    MessageInput(on_wrong_type_attachment_upload, content_types=[ContentType.ANY]),
    Row(
        Next(Const("✅ Завершить")),
        Cancel(Const("❌ Отмена")),
    ),
    state=FeedbackUserSG.attachment,
)


feedback_end_window = Window(
    Format("Ваш отзыв отправлен! Спасибо за обратную связь ✅"),
    Row(Cancel(Const("❌ Отмена")), Button(Const("На главную"), id="finish")),
    state=FeedbackUserSG.end,
)

dialog = Dialog(feedback_text_window, feedback_attachment_window, feedback_end_window)
