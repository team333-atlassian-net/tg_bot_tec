import logging

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Button

from dao.org_structure import add_org_structure
from states import OrgStructureCreationSG


logger = logging.getLogger(__name__)


async def on_title_input(message: Message, widget: TextInput, dialog: DialogManager):
    """
    Обрабатывает ввод названия организационной структуры.
    Сохраняет введённый текст в dialog_data и переходит к описанию.
    """
    dialog.dialog_data["title"] = message.text
    await dialog.switch_to(OrgStructureCreationSG.description)


async def on_description_input(
    message: Message, widget: TextInput, dialog: DialogManager
):
    """
    Обрабатывает ввод описания организационной структуры.
    Сохраняет описание и переходит к загрузке файла.
    """
    dialog.dialog_data["description"] = message.text
    await dialog.switch_to(OrgStructureCreationSG.file)


async def on_file_input(message: Message, widget, dialog: DialogManager):
    """
    Обрабатывает загрузку документа.
    Сохраняет file_id и имя файла. Переходит к окну подтверждения.
    """
    file_id = None
    file_name = None
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name

    if file_id:
        dialog.dialog_data["file_id"] = file_id
        dialog.dialog_data["file_name"] = file_name
        await dialog.switch_to(OrgStructureCreationSG.confirm)
    else:
        await message.answer("❌ Пожалуйста, отправьте файл.")


async def on_description_skip(callback: CallbackQuery, button, dialog: DialogManager):
    """
    Обрабатывает нажатие кнопки "Пропустить" на этапе описания.
    Устанавливает значение описания в None и переходит к загрузке файла.
    """
    dialog.dialog_data["description"] = None
    await dialog.switch_to(OrgStructureCreationSG.file)


async def on_file_skip(callback: CallbackQuery, button, dialog: DialogManager):
    """
    Обрабатывает нажатие кнопки "Пропустить" на этапе загрузки файла.
    Устанавливает file_id в None и переходит к окну подтверждения.
    """
    dialog.dialog_data["file_id"] = None
    await dialog.switch_to(OrgStructureCreationSG.confirm)


async def on_confirm_press(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Обрабатывает подтверждение создания новой оргструктуры.
    Сохраняет данные в БД и завершает диалог.
    """
    title = dialog_manager.dialog_data.get("title")
    description = dialog_manager.dialog_data.get("description")
    file_id = dialog_manager.dialog_data.get("file_id")

    if not title:
        await callback.message.answer("❌ Не удалось получить название.")
        return

    await add_org_structure(title, description, file_id)
    await callback.message.answer(
        "✅ Информация об организационной структуре добавлена"
    )
    logger.info("Администратор добавил новую информацию об оргструктуре (/add_event)")
    await dialog_manager.done()
