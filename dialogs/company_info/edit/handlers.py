import logging
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Radio, ScrollingGroup
from dao.company_info import (
    delete_company_info,
    update_company_info,
)
from states import ManageCompanyInfoSG

logger = logging.getLogger(__name__)


async def on_company_info_selected(
    callback: CallbackQuery, widget, manager: DialogManager, item_id: str
):
    """
    Сохраняет выбранный раздел и переключается на детали.
    """
    manager.dialog_data["company_info_id"] = item_id
    await manager.switch_to(ManageCompanyInfoSG.company_info_action)


async def on_edit_title_start(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Переход к окну редактирования названия.
    """
    await dialog_manager.switch_to(ManageCompanyInfoSG.edit_title)


async def on_edit_description_start(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Переход к окну редактирования описания.
    """
    await dialog_manager.switch_to(ManageCompanyInfoSG.edit_description)


async def on_edit_title(
    message: Message, value: TextInput, dialog_manager: DialogManager, widget
):
    """
    Сохраняет новое название и завершает диалог.
    """
    company_info_id = dialog_manager.dialog_data.get("company_info_id")
    if company_info_id:
        await update_company_info(int(company_info_id), value.get_value(), None)
        await message.answer("✏️ Название обновлено.")
        logger.info("Админ обновил название (/manage_company_info)")
        await dialog_manager.switch_to(ManageCompanyInfoSG.company_info_action)
    await dialog_manager.done()


async def on_edit_description(
    message: Message, value: TextInput, dialog_manager: DialogManager, widget
):
    """
    Сохраняет новое описание и завершает диалог.
    """
    company_info_id = dialog_manager.dialog_data.get("company_info_id")
    if company_info_id:
        await update_company_info(int(company_info_id), None, value.get_value())
        await message.answer("📝 Описание обновлено.")
        logger.info("Админ обновил описание (/manage_company_info)")
        await dialog_manager.switch_to(ManageCompanyInfoSG.company_info_action)
    await dialog_manager.done()


async def on_file_edit(message: Message, widget, dialog_manager: DialogManager):
    """
    Сохраняет новый файл и завершает диалог.
    """
    company_info_id = dialog_manager.dialog_data.get("company_info_id")
    file_id = None
    if message.document:
        file_id = message.document.file_id

    if file_id and company_info_id:
        await update_company_info(int(company_info_id), None, None, file_id=file_id)
        await message.answer("📎 Файл обновлён.")
        logger.info("Админ обновил файл (/manage_company_info)")
        await dialog_manager.switch_to(ManageCompanyInfoSG.company_info_action)
    else:
        await message.answer("❌ Пожалуйста, отправьте документ.")


async def on_image_edit(message: Message, widget, dialog_manager: DialogManager):
    """
    Обрабатывает загрузку нового изображения или документа для CompanyInfo.
    Сохраняет file_id и завершает диалог.
    """
    company_info_id = dialog_manager.dialog_data.get("company_info_id")
    image_id = None

    if message.photo:
        image_id = message.photo[-1].file_id  # Самое большое по размеру фото

    if image_id and company_info_id:
        await update_company_info(
            int(company_info_id), None, None, None, image_id=image_id
        )
        await message.answer("📎 Изображение обновлено.")
        logger.info("Админ обновил фото (/manage_company_info)")
        await dialog_manager.switch_to(ManageCompanyInfoSG.company_info_action)
    else:
        await message.answer("❌ Пожалуйста, отправьте изображение.")


async def on_delete_company_info(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Удаляет выбранное мероприятие.
    """
    company_info_id = dialog_manager.dialog_data.get("company_info_id")
    if company_info_id:
        await delete_company_info(int(company_info_id))
        await callback.message.answer("✅ Информация удалена.")
        logger.info("Администратор удалил информацию о компании (/manage_company_info)")
        await dialog_manager.switch_to(ManageCompanyInfoSG.list)

    await dialog_manager.done()


async def on_exit(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Выход из режима редактирования.
    """
    await callback.message.answer("❌ Вы вышли из режима редактирования.")
    await dialog_manager.done()
