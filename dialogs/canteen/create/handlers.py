import logging
from datetime import datetime

from aiogram.types import Message, CallbackQuery

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput

from dao.canteen import add_canteen_menu_info, add_canteen_info
from models import CanteenMenuFileType
from states import CanteenInfoCreationSG

logger = logging.getLogger(__name__)


# Столовая


async def on_start_time_input(
    message: Message, widget: TextInput, dialog: DialogManager
):
    """
    Обработка ввода времени начала работы столовой.
    Валидирует формат HH:MM.
    """
    try:
        time = datetime.strptime(message.text.strip(), "%H:%M").time()
    except ValueError:
        await message.answer(
            "❌ Неверный формат времени. Введите в формате HH:MM, например: 10:30"
        )
        return
    dialog.dialog_data["start_time"] = message.text.strip()
    await dialog.switch_to(CanteenInfoCreationSG.end_time)


async def on_end_time_input(message: Message, widget: TextInput, dialog: DialogManager):
    """
    Обработка ввода времени окончания работы столовой.
    Валидирует формат HH:MM.
    """
    try:
        time = datetime.strptime(message.text.strip(), "%H:%M").time()
    except ValueError:
        await message.answer(
            "❌ Неверный формат времени. Введите в формате HH:MM, например: 15:00"
        )
        return
    dialog.dialog_data["end_time"] = message.text.strip()
    await dialog.switch_to(CanteenInfoCreationSG.description)


async def on_canteen_description_input(
    message: Message, widget: TextInput, dialog: DialogManager
):
    """
    Обработка описания столовой (необязательное поле).
    """
    dialog.dialog_data["description"] = message.text.strip()
    await dialog.switch_to(CanteenInfoCreationSG.confirm_canteen)


async def on_canteen_confirm(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Подтверждение и сохранение информации о столовой в базу данных.
    """
    data = dialog_manager.dialog_data
    try:
        start = datetime.strptime(data["start_time"], "%H:%M").time()
        end = datetime.strptime(data["end_time"], "%H:%M").time()
    except Exception:
        await callback.message.answer(
            "❌ Ошибка преобразования времени. Повторите ввод."
        )
        return

    description = data.get("description")
    await add_canteen_info(start, end, description)
    await callback.message.answer("✅ Информация о столовой сохранена.")
    logger.info("Администратор добавил информацию о столовой (/add_canteen_info)")
    await dialog_manager.done()


# Меню


async def on_menu_date_input(
    message: Message, widget: TextInput, dialog: DialogManager
):
    """
    Обработка ввода даты меню. Валидирует формат YYYY-MM-DD.
    """
    try:
        date = datetime.strptime(message.text.strip(), "%Y-%m-%d").date()
    except ValueError:
        await message.answer(
            "❌ Неверный формат даты. Введите в формате ГГГГ-ММ-ДД, например: 2025-08-01"
        )
        return
    dialog.dialog_data["date"] = message.text.strip()
    await dialog.switch_to(CanteenInfoCreationSG.menu_text)


async def on_menu_text_input(
    message: Message, widget: TextInput, dialog: DialogManager
):
    """Обработка текста меню (необязательное поле)."""
    dialog.dialog_data["menu"] = message.text.strip()
    await dialog.switch_to(CanteenInfoCreationSG.menu_file)


async def on_menu_file_input(message: Message, widget, dialog: DialogManager):
    """Обработка загружаемого файла меню или фотографии."""
    file_id = None
    file_name = None
    if message.document:
        file_name = message.document.file_name
        file_id = message.document.file_id
        file_type = CanteenMenuFileType.FILE
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_name = "Фото меню"
        file_type = CanteenMenuFileType.PHOTO
    else:
        file_id = None
        file_type = None
    dialog.dialog_data["file_id"] = file_id
    dialog.dialog_data["file_name"] = file_name
    dialog.dialog_data["file_type"] = file_type
    await dialog.switch_to(CanteenInfoCreationSG.confirm_menu)


async def on_menu_confirm(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Подтверждение и сохранение информации о меню в базу данных.
    Требует наличие либо текста, либо файла.
    """
    data = dialog_manager.dialog_data
    try:
        date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    except Exception:
        await callback.message.answer("❌ Ошибка преобразования даты.")
        return

    menu = data.get("menu")
    file_id = data.get("file_id")
    file_type = data.get("file_type")

    if not menu and not file_id:
        await callback.message.answer(
            "❌ Укажите хотя бы текст меню или прикрепите файл."
        )
        await dialog_manager.switch_to(CanteenInfoCreationSG.menu_text)
        return

    await add_canteen_menu_info(date, menu, file_id, file_type)
    await callback.message.answer("✅ Меню добавлено.")
    logger.info(f"Администратор добавил меню на {date} (/add_canteen_info)")
    await dialog_manager.done()


# Обработчики пропусков


async def on_description_skip(callback: CallbackQuery, button, dialog: DialogManager):
    """Пропуск описания столовой."""
    dialog.dialog_data["description"] = None
    await dialog.switch_to(CanteenInfoCreationSG.confirm_canteen)


async def on_menu_skip(callback: CallbackQuery, button, dialog: DialogManager):
    """Пропуск текста меню."""
    dialog.dialog_data["menu"] = None
    await dialog.switch_to(CanteenInfoCreationSG.menu_file)


async def on_file_skip(callback: CallbackQuery, button, dialog: DialogManager):
    """Пропуск файла меню."""
    dialog.dialog_data["file_id"] = None
    await dialog.switch_to(CanteenInfoCreationSG.confirm_menu)
