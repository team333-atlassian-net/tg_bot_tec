import logging

from aiogram_dialog import DialogManager


logger = logging.getLogger(__name__)


async def get_confirm_data(dialog_manager: DialogManager, **kwargs):
    """
    Подготавливает данные для окна подтверждения.
    """
    return {
        "first_name": dialog_manager.dialog_data.get("first_name", "-"),
        "last_name": dialog_manager.dialog_data.get("last_name", "-"),
        "middle_name": dialog_manager.dialog_data.get("middle_name", "-"),
    }
