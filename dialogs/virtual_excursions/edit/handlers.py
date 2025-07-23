import logging
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.api.protocols import DialogManager
from aiogram.types import Message
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Select,
)
from dao.virtual_excursions import *
from states import ExcursionEditSG, ExcursionCreationSG


async def on_virtex_selected(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["selected_virtex_id"] = int(selected_id)
    await manager.switch_to(ExcursionEditSG.detail)


async def on_material_selected(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["selected_material_id"] = int(selected_id)
    await manager.switch_to(ExcursionEditSG.material)


async def on_press_edit_virtex_title(callback, button: Button, dialog: DialogManager):
    await dialog.switch_to(ExcursionEditSG.edit_title)


async def on_edit_virtex_title(
    message: Message, widget: TextInput, dialog: DialogManager
):
    virtex_id = dialog.dialog_data["selected_virtex_id"]
    await update_virtex_title(virtex_id=virtex_id, new_title=message.text)
    message.answer("✅ Название экскурсии успешно обновлено!")
    await dialog.switch_to(ExcursionEditSG.detail)


async def on_press_edit_virtex_description(
    callback, button: Button, dialog: DialogManager
):
    await dialog.switch_to(ExcursionEditSG.edit_description)


async def on_edit_virtex_description(
    message: Message, widget: TextInput, dialog: DialogManager
):
    virtex_id = dialog.dialog_data["selected_virtex_id"]
    await update_virtex_description(virtex_id=virtex_id, new_description=message.text)
    message.answer("✅ Описание экскурсии успешно обновлено!")
    await dialog.switch_to(ExcursionEditSG.detail)


async def on_press_edit_material_name(callback, button: Button, dialog: DialogManager):
    await dialog.switch_to(ExcursionEditSG.edit_material_name)


async def on_edit_material_name(
    message: Message, widget: TextInput, dialog: DialogManager
):
    material_id = dialog.dialog_data["selected_material_id"]
    await update_material_name(material_id=material_id, new_name=message.text)
    message.answer("✅ Навзвание материала успешно обновлено!")
    await dialog.switch_to(ExcursionEditSG.detail)


async def on_press_edit_material(callback, button: Button, dialog: DialogManager):
    await dialog.switch_to(ExcursionEditSG.edit_material)


async def on_edit_material(
    message: Message, widget: MessageInput, dialog: DialogManager
):
    material_id = dialog.dialog_data["selected_material_id"]
    if not message.document and not message.text:
        return
    doc = message.document
    text = message.text
    file_id = doc.file_id if doc else None
    await update_material(
        material_id=material_id, new_telegram_file_id=file_id, new_text=text
    )
    await message.answer("Материал успешно обновлен")


async def on_press_add_material(callback, button: Button, dialog: DialogManager):
    data = {"virtex_id": dialog.dialog_data["selected_virtex_id"]}
    await dialog.start(state=ExcursionCreationSG.material_name, data=data)


async def on_press_delete_virtex(callback, button: Button, dialog: DialogManager):
    await dialog.switch_to(ExcursionEditSG.delete_virtex)


async def on_press_delete_material(callback, button: Button, dialog: DialogManager):
    await dialog.switch_to(ExcursionEditSG.delete_material)


async def on_delete_virtex(callback, button: Button, dialog: DialogManager):
    virtex_id = dialog.dialog_data["selected_virtex_id"]
    await delete_virtex(virtex_id=virtex_id)
    await dialog.switch_to(ExcursionEditSG.list)


async def on_delete_material(callback, button: Button, dialog: DialogManager):
    material_id = dialog.dialog_data["selected_material_id"]
    await delete_material(material_id=material_id)
    await dialog.switch_to(ExcursionEditSG.detail)
