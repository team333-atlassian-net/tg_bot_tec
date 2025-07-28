import io
import logging
import pandas as pd

from aiogram_dialog import Dialog, Window, DialogManager


logger = logging.getLogger(__name__)


async def get_confirm_data(dialog_manager: DialogManager, **kwargs):
    """
    Геттер данных для окна подтверждения.
    Возвращает все данные диалога для отображения пользователю.
    """
    return {
        "dialog_data": dialog_manager.dialog_data,
    }
