import logging

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Button

from dao.company_info import add_company_info
from states import CompanyInfoCreationSG

logger = logging.getLogger(__name__)


async def on_title_input(message: Message, widget: TextInput, dialog: DialogManager):
    """
    Обрабатывает ввод названия организационной структуры.
    Сохраняет введённый текст в dialog_data и переходит к описанию.
    """
    dialog.dialog_data["title"] = message.text
    await dialog.switch_to(CompanyInfoCreationSG.description)


async def on_description_input(
    message: Message, widget: TextInput, dialog: DialogManager
):
    """
    Обрабатывает ввод описания организационной структуры.
    Сохраняет описание и переходит к загрузке файла.
    """
    dialog.dialog_data["description"] = message.text
    await dialog.switch_to(CompanyInfoCreationSG.file)


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
        await dialog.switch_to(CompanyInfoCreationSG.image)
    else:
        await message.answer("❌ Пожалуйста, отправьте файл.")


async def on_image_input(message: Message, widget, dialog: DialogManager):
    """
    Обрабатывает загрузку изображения.
    Сохраняет image_id в dialog_data, затем переходит к подтверждению.
    """
    image_id = None
    image_name = None

    # Обработка фото (message.photo — список разных размеров)
    if message.photo:
        image_id = message.photo[-1].file_id  # Самое большое доступное фото
        image_name = "Фото"
    if image_id:
        dialog.dialog_data["image_id"] = image_id
        dialog.dialog_data["image_name"] = image_name
        await dialog.switch_to(CompanyInfoCreationSG.confirm)
    else:
        await message.answer("❌ Пожалуйста, отправьте изображение.")


async def on_description_skip(callback: CallbackQuery, button, dialog: DialogManager):
    """
    Обрабатывает нажатие кнопки "Пропустить" на этапе описания.
    Устанавливает значение описания в None и переходит к загрузке файла.
    """
    dialog.dialog_data["description"] = None
    await dialog.switch_to(CompanyInfoCreationSG.file)


async def on_file_skip(callback: CallbackQuery, button, dialog: DialogManager):
    """
    Обрабатывает нажатие кнопки "Пропустить" на этапе загрузки файла.
    Устанавливает file_id в None и переходит к окну подтверждения.
    """
    dialog.dialog_data["file_id"] = None
    await dialog.switch_to(CompanyInfoCreationSG.image)


async def on_image_skip(callback: CallbackQuery, button, dialog: DialogManager):
    """
    Обрабатывает нажатие кнопки "Пропустить" на этапе загрузки фото.
    Устанавливает image_id в None и переходит к окну подтверждения.
    """
    dialog.dialog_data["image_id"] = None
    await dialog.switch_to(CompanyInfoCreationSG.confirm)


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
    image_id = dialog_manager.dialog_data.get("image_id")

    if not title:
        await callback.message.answer("❌ Не удалось получить название.")
        return

    await add_company_info(title, description, file_id, image_id)
    await callback.message.answer("✅ Информация о компании добавлена")
    logger.info("Администратор добавил новую информацию о компании (/add_company_info)")
    await dialog_manager.done()
