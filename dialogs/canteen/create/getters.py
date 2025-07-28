import logging

from aiogram_dialog import DialogManager

logger = logging.getLogger(__name__)


async def get_canteen_confirm_data(dialog_manager: DialogManager, **kwargs):
    """
    Подготавливает данные для окна подтверждения информации о столовой.
    """
    return {
        "start": dialog_manager.dialog_data.get("start_time"),
        "end": dialog_manager.dialog_data.get("end_time"),
        "description": dialog_manager.dialog_data.get("description") or "-",
    }


async def get_menu_confirm_data(dialog_manager: DialogManager, **kwargs):
    return {
        "date": dialog_manager.dialog_data.get("date"),
        "menu": dialog_manager.dialog_data.get("menu") or "-",
        "file_name": dialog_manager.dialog_data.get("file_name") or "-",
    }
