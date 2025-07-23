import logging
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.api.protocols import DialogManager
from aiogram.types import Message
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
)
from dao.virtual_excursions import *
from states import ExcursionCreationSG

logger = logging.getLogger(__name__)


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
    await dialog.switch_to(ExcursionCreationSG.description)


async def on_description_input(
    message: Message, widget: TextInput, dialog: DialogManager
):
    """
    Обработчик ввода описания.

    """
    dialog.dialog_data["description"] = message.text
    await dialog.switch_to(ExcursionCreationSG.confirm)


async def on_description_skip(callback, button: Button, dialog: DialogManager):
    dialog.dialog_data["description"] = "—"
    await dialog.switch_to(ExcursionCreationSG.confirm)


async def on_document_upload(
    message: Message, widget: MessageInput, dialog: DialogManager
):
    """
    Обработчик добавления документов и текстового описания.

    """
    if not message.document and not message.text:
        return
    name = dialog.dialog_data["material_name"]
    doc = message.document
    text = message.text
    virtex_id = dialog.dialog_data.get("virtex_id") or dialog.start_data.get(
        "virtex_id"
    )  # start_data для случая вызова из edit диалога
    file_id = doc.file_id if doc else None
    await add_material(virtex_id, file_id, name, text)
    await dialog.switch_to(ExcursionCreationSG.material_end)


async def on_confirm_press(callback, button, manager: DialogManager):
    title = manager.dialog_data.get("title")
    description = manager.dialog_data.get("description")

    virtex = await create_virtex(title, description)

    manager.dialog_data["virtex_id"] = virtex.id
    await manager.switch_to(ExcursionCreationSG.material_name)


async def on_material_name_input(
    message: Message,
    widget: TextInput,
    manager: DialogManager,
):
    manager.dialog_data["material_name"] = message.text
    await manager.switch_to(ExcursionCreationSG.upload_materials)
