import logging
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram.types import Message, CallbackQuery
from aiogram_dialog.widgets.kbd import Button
from states import FeedbackUserSG
from dao.feedback import *
from dao.auth import get_user

logger = logging.getLogger(__name__)


async def on_text_input(
    message: Message, widget: TextInput, dialog: DialogManager, data
):
    text = message.text
    tg_id = message.from_user.id
    user = await get_user(tg_id=tg_id)
    feedback = await create_feedback(user.id, text)
    dialog.dialog_data["feedback_id"] = feedback.id
    await dialog.switch_to(FeedbackUserSG.attachment)


async def on_attachment_upload(
    message: Message, widget: MessageInput, dialog: DialogManager
):
    file = message.photo[0]
    file_id = file.file_id
    feedback_id = dialog.dialog_data["feedback_id"]
    await add_feedback_attachment(feedback_id=feedback_id, file_id=file_id)


async def on_wrong_type_attachment_upload(
    message: Message, widget: MessageInput, dialog: DialogManager
):
    await message.answer("Пожалуйста, прикрепите фото")
