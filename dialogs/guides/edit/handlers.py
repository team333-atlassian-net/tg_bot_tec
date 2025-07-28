import logging
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.api.protocols import DialogManager
from aiogram.types import Message
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Select,
)
from dao.guides import *
from states import GuideCreationSG, GuideEditSG


async def on_doc_select(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["doc"] = manager.dialog_data["docs"][int(selected_id)]
    await manager.switch_to(GuideEditSG.guides)


async def on_guide_select(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["guide_id"] = int(selected_id)
    await manager.switch_to(GuideEditSG.guide)


async def on_press_edit_doc_name(callback, button: Button, dialog: DialogManager):
    await dialog.switch_to(GuideEditSG.edit_doc_name)


async def on_edit_doc_name(message: Message, widget: TextInput, dialog: DialogManager):
    old_name = dialog.dialog_data["doc"]
    new_name = message.text
    await update_doc_name(old_doc_name=old_name, new_doc_name=new_name)
    message.answer("✅ Название документа успешно обновлено!")
    dialog.dialog_data["doc"] = new_name
    await dialog.switch_to(GuideEditSG.guides)


async def on_press_edit_guide_title(callback, button: Button, dialog: DialogManager):
    await dialog.switch_to(GuideEditSG.edit_title)


async def on_edit_guide_title(
    message: Message, widget: TextInput, dialog: DialogManager
):
    guide_id = dialog.dialog_data["guide_id"]
    await update_guide_title(guide_id=guide_id, new_title=message.text)
    message.answer("✅ Название инструкции успешно обновлено!")
    await dialog.switch_to(GuideEditSG.guides)


async def on_press_edit_guide_content(callback, button: Button, dialog: DialogManager):
    await dialog.switch_to(GuideEditSG.edit_content)


async def on_edit_guide_content(
    message: Message, widget: MessageInput, dialog: DialogManager
):
    guide_id = dialog.dialog_data["guide_id"]
    if not message.document and not message.text:
        return
    file = message.document
    text = message.text
    file_id = file.file_id if file else None
    await update_guide_content(guide_id=guide_id, new_file_id=file_id, new_text=text)
    await message.answer("✅ Инструкция успешно обновлена!")
    await dialog.switch_to(GuideEditSG.guides)


async def on_press_add_guide(callback, button: Button, dialog: DialogManager):
    data = {"doc": dialog.dialog_data["doc"]}
    await dialog.start(state=GuideCreationSG.title, data=data)


async def on_press_delete_doc(callback, button: Button, dialog: DialogManager):
    await dialog.switch_to(GuideEditSG.delete_doc)


async def on_delete_doc(callback, button: Button, dialog: DialogManager):
    doc = dialog.dialog_data["doc"]
    await delete_all_guide_by_document(doc)
    await dialog.switch_to(GuideEditSG.documents)


async def on_press_delete_guide(callback, button: Button, dialog: DialogManager):
    await dialog.switch_to(GuideEditSG.delete_guide)


async def on_delete_guide(callback, button: Button, dialog: DialogManager):
    guide_id = dialog.dialog_data["guide_id"]
    await delete_guide(guide_id=guide_id)
    await dialog.switch_to(GuideEditSG.guides)
