import logging

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput

from dao.org_structure import (
    delete_org_structure,
    update_org_structure,
)
from states import ManageOrgStructureSG

logger = logging.getLogger(__name__)


async def on_org_structure_selected(
    callback: CallbackQuery, widget, manager: DialogManager, item_id: str
):
    """
    Сохраняет выбранный раздел и переключается на детали.
    """
    manager.dialog_data["org_structure_id"] = item_id
    await manager.switch_to(ManageOrgStructureSG.org_structure_action)


async def on_edit_title_start(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Переход к окну редактирования названия.
    """
    await dialog_manager.switch_to(ManageOrgStructureSG.edit_title)


async def on_edit_description_start(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Переход к окну редактирования описания.
    """
    await dialog_manager.switch_to(ManageOrgStructureSG.edit_description)


async def on_edit_title(
    message: Message, value: TextInput, dialog_manager: DialogManager, widget
):
    """
    Сохраняет новое название и завершает диалог.
    """
    org_structure_id = dialog_manager.dialog_data.get("org_structure_id")
    if org_structure_id:
        await update_org_structure(int(org_structure_id), value.get_value(), None)
        await message.answer("✏️ Название обновлено.")
        logger.info("Админ обновил название (/manage_org_structures)")
    await dialog_manager.switch_to(ManageOrgStructureSG.org_structure_action)


async def on_edit_description(
    message: Message, value: TextInput, dialog_manager: DialogManager, widget
):
    """
    Сохраняет новое описание и завершает диалог.
    """
    org_structure_id = dialog_manager.dialog_data.get("org_structure_id")
    if org_structure_id:
        await update_org_structure(int(org_structure_id), None, value.get_value())
        await message.answer("📝 Описание обновлено.")
        logger.info("Админ обновил описание (/manage_org_structures)")
    await dialog_manager.switch_to(ManageOrgStructureSG.org_structure_action)


async def on_edit_file(message: Message, widget, dialog_manager: DialogManager):
    """
    Сохраняет новый файл и завершает диалог.
    """
    org_structure_id = dialog_manager.dialog_data.get("org_structure_id")
    file_id = None
    if message.document:
        file_id = message.document.file_id

    if file_id and org_structure_id:
        await update_org_structure(int(org_structure_id), None, None, file_id=file_id)
        await message.answer("📎 Файл обновлён.")
        logger.info("Админ обновил файл (/manage_org_structures)")
        await dialog_manager.switch_to(ManageOrgStructureSG.org_structure_action)
    else:
        await message.answer("❌ Пожалуйста, отправьте документ.")


async def on_delete_org_structure(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Удаляет выбранное мероприятие.
    """
    org_structure_id = dialog_manager.dialog_data.get("org_structure_id")
    if org_structure_id:
        await delete_org_structure(int(org_structure_id))
        await callback.message.answer("✅ Раздел организационной структур удален.")
        logger.info("Администратор удалил мероприятие (/manage_org_structures)")
    await dialog_manager.switch_to(ManageOrgStructureSG.list)


async def on_exit(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Выход из режима редактирования.
    """
    await callback.message.answer("❌ Вы вышли из режима редактирования.")
    await dialog_manager.done()
