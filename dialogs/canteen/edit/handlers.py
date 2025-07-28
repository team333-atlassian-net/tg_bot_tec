import logging

from datetime import datetime, date
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput

from dao.canteen import *
from models import CanteenMenuFileType
from states import ManageCanteenSG

logger = logging.getLogger(__name__)


async def on_edit_start_time_start(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Переходит к окну ввода нового времени начала работы столовой.
    """
    await dialog_manager.switch_to(ManageCanteenSG.edit_start_time)


async def on_edit_start_time(
    message: Message, value: TextInput, dialog_manager: DialogManager, widget
):
    """
    Сохраняет новое время начала работы столовой.
    """
    start_time_text = value.get_value()
    try:
        time = datetime.strptime(start_time_text, "%H:%M").time()
    except ValueError:
        await message.answer(
            "❌ Неверный формат времени. Введите в формате HH:MM, например: 10:00"
        )
        return

    await update_canteen_info(start=time, end=None, description=None)
    await message.answer("✏️ Время начала работы столовой обновлено.")
    logger.info(
        "Администратор обновил время начала работы столовой (/manage_canteen_info)"
    )
    await dialog_manager.switch_to(ManageCanteenSG.canteen_info_action)


async def on_edit_end_time_start(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Переход к окну редактирования времени окончания работы.
    """
    await dialog_manager.switch_to(ManageCanteenSG.edit_end_time)


async def on_edit_end_time(
    message: Message, value: TextInput, dialog_manager: DialogManager, widget
):
    """
    Сохраняет новое время окончания работы столовой.
    """
    end_time_text = value.get_value()
    try:
        time = datetime.strptime(end_time_text, "%H:%M").time()
    except ValueError:
        await message.answer(
            "❌ Неверный формат времени. Введите в формате HH:MM, например: 16:00"
        )
        return

    await update_canteen_info(start=None, end=time, description=None)
    await message.answer("✏️ Время завершения работы столовой обновлено.")
    logger.info(
        "Администратор обновил время авершения работы столовой (/manage_canteen_info)"
    )
    await dialog_manager.switch_to(ManageCanteenSG.canteen_info_action)


async def on_edit_description(
    message: Message, value: TextInput, dialog_manager: DialogManager, widget
):
    """
    Обновляет описание столовой.
    """
    await update_canteen_info(None, None, value.get_value())
    await message.answer("✏️ Описание столовой обновлено.")
    logger.info("Администратор обновил описание столовой (/manage_canteen_info)")
    await dialog_manager.switch_to(ManageCanteenSG.canteen_info_action)


async def on_delete_canteen_info(
    callback: CallbackQuery, widget, dialog_manager: DialogManager
):
    """
    Удаляет всю информацию о столовой.
    """
    await delete_canteen_info()
    await callback.message.answer("❌ Информация о столовой удалена.")
    logger.info("Администратор удалил информацию о столовой (/manage_canteen_info)")
    await dialog_manager.switch_to(ManageCanteenSG.choice)


async def on_select_menu(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, selected_id: str
):
    """
    Обработка выбора меню по ID из списка.
    """
    menu = await get_canteen_menu_by_id(int(selected_id))
    dialog_manager.dialog_data["selected_menu"] = menu
    dialog_manager.dialog_data["menu_id"] = menu.id
    await dialog_manager.switch_to(ManageCanteenSG.menu_edit_action)


async def on_select_menu_by_date(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, selected_date: date
):
    """
    Обработка выбора меню по дате (из календаря).
    """
    menu = await get_canteen_menu_by_date(selected_date)
    if not menu:
        await callback.message.answer("❌ На выбранную дату меню не найдено.")
        return
    dialog_manager.dialog_data["selected_menu"] = menu
    dialog_manager.dialog_data["menu_id"] = menu.id
    await dialog_manager.switch_to(ManageCanteenSG.menu_edit_action)


async def on_edit_menu_text(
    message: Message, input: TextInput, dialog_manager: DialogManager, widget
):
    """
    Обновляет текст меню.
    """
    new_text = input.get_value()
    menu_id = dialog_manager.dialog_data.get("menu_id")
    await update_canteen_menu(menu_id, None, new_text, None, None)

    updated_menu = await get_canteen_menu_by_id(menu_id)
    dialog_manager.dialog_data["selected_menu"] = updated_menu

    await message.answer("✏️ Текст меню обновлён.")
    logger.info("Администратор обновил меню столовой (/manage_canteen_info)")
    await dialog_manager.switch_to(ManageCanteenSG.menu_edit_action)


async def on_edit_menu_file(message: Message, widget, dialog_manager: DialogManager):
    """
    Обновляет файл (документ/изображение) для выбранного меню.
    """
    if not message.document and not message.photo:
        await message.answer("❌ Пришлите файл (документ или изображение).")
        return

    file_id = None
    file_type = None
    if message.document:
        file_id = message.document.file_id
        file_type = CanteenMenuFileType.FILE
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_type = CanteenMenuFileType.PHOTO

    menu_id = dialog_manager.dialog_data.get("menu_id")
    await update_canteen_menu(menu_id, None, None, file_id=file_id, file_type=file_type)
    updated_menu = await get_canteen_menu_by_id(menu_id)
    dialog_manager.dialog_data["selected_menu"] = updated_menu

    await message.answer("📎 Файл меню обновлён.")
    logger.info("Администратор обновил файл меню столовой (/manage_canteen_info)")
    await dialog_manager.switch_to(ManageCanteenSG.menu_edit_action)


async def on_delete_menu_file(
    callback: CallbackQuery, widget, dialog_manager: DialogManager
):
    """
    Удаляет прикреплённый файл у выбранного меню.
    """
    menu_id = dialog_manager.dialog_data.get("menu_id")
    await delete_canteen_menu_file(menu_id)
    updated_menu = await get_canteen_menu_by_id(menu_id)
    dialog_manager.dialog_data["selected_menu"] = updated_menu

    await callback.message.answer("🗑 Файл меню удалён.")
    await dialog_manager.show()


async def on_delete_menu(
    callback: CallbackQuery, widget, dialog_manager: DialogManager
):
    """
    Удаляет выбранное меню.
    """
    menu_id = dialog_manager.dialog_data.get("menu_id")
    if not menu_id:
        await callback.message.answer("❌ Меню не выбрано.")
        return

    await delete_canteen_menu(menu_id)
    await callback.message.answer("🗑 Меню удалено.")
    logger.info(f"Администратор удалил меню с id={menu_id} (/manage_canteen_info)")
    await dialog_manager.switch_to(ManageCanteenSG.select_menu)
