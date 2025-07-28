import logging
from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from dao.canteen import (
    get_all_canteen_menu,
    get_canteen_menu_by_id,
)
from models import CanteenMenuFileType
from states import CanteenViewSG

logger = logging.getLogger(__name__)


async def on_menu_selected(
    callback: CallbackQuery, widget, manager: DialogManager, selected_id: str
):
    """
    Загружает выбранное меню по ID, сохраняет его в dialog_data и отображает файл.
    """
    menu = await get_canteen_menu_by_id(int(selected_id))
    manager.dialog_data["canteen_menu"] = menu
    manager.dialog_data["selected_menu_id"] = selected_id

    # Отправляем файл пользователю в зависимости от его типа
    if menu and menu.file_id:
        if menu.file_type == CanteenMenuFileType.PHOTO:
            await callback.message.answer_photo(menu.file_id)
        else:
            await callback.message.answer_document(menu.file_id)

    await manager.switch_to(CanteenViewSG.menu_detail)


async def on_date_selected(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, selected_date: date
):
    """
    Ищет меню по выбранной дате, отправляет файл и переходит к окну с деталями.
    """
    menus = await get_all_canteen_menu()
    selected = next((m for m in menus if m.date == selected_date), None)
    if not selected:
        await callback.message.answer("❌ Меню на эту дату не найдено.")
        return

    dialog_manager.dialog_data["canteen_menu"] = selected
    dialog_manager.dialog_data["selected_menu_id"] = selected.id

    if selected.file_id:
        if selected.file_type == CanteenMenuFileType.PHOTO:
            await callback.message.answer_photo(selected.file_id)
        else:
            await callback.message.answer_document(selected.file_id)

    await dialog_manager.switch_to(CanteenViewSG.menu_detail)
