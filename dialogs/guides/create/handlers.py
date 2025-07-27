import logging
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.api.protocols import DialogManager
from aiogram.types import Message, CallbackQuery
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Select,
)
from dao.guides import *
from states import GuideCreationSG

logger = logging.getLogger(__name__)


async def on_doc_selected(
    callback: CallbackQuery, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["doc"] = widget.items[selected_id][1]
    await manager.switch_to(GuideCreationSG.title)


async def on_doc_name_input(message: Message, widget: Select, manager: DialogManager):
    manager.dialog_data["doc"] = message.text
    await manager.switch_to(GuideCreationSG.title)


async def on_title_input(
    message: Message,
    widget: TextInput,
    dialog: DialogManager,
):
    """
    Обработчик успешного ввода заголовка.

    Сохраняет заголовок в dialog_data и переключается на состояние ввода описания.
    """
    dialog.dialog_data["title"] = message.text
    await dialog.switch_to(GuideCreationSG.upload_content)


async def on_guide_content_upload(
    message: Message, widget: MessageInput, dialog: DialogManager
):
    """
    Обработчик добавления документов и текстового описания.

    """
    if not message.document and not message.text:
        return

    if not dialog.dialog_data.get("doc"):
        dialog.dialog_data["doc"] = dialog.start_data.get(
            "doc"
        )  # start_data для случая вызова из edit диалога

    title = dialog.dialog_data["title"]
    doc = dialog.dialog_data["doc"]
    file = message.document
    text = message.text
    file_id = file.file_id if file else None
    await create_guide(document=doc, title=title, text=text, file_id=file_id)
    await dialog.switch_to(GuideCreationSG.end)
