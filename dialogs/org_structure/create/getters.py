import logging

from aiogram_dialog import DialogManager

logger = logging.getLogger(__name__)


async def get_confirm_data(dialog_manager: DialogManager, **kwargs):
    """
    Подготавливает данные для отображения в окне подтверждения.
    Возвращает название, описание (или '-') и имя файла (или '-').
    """
    title = dialog_manager.dialog_data.get("title")
    description = dialog_manager.dialog_data.get("description")
    file_name = dialog_manager.dialog_data.get("file_name")

    file_text = file_name if file_name else "-"
    description_text = description if description else "-"

    return {
        "dialog_data": {
            "title": title,
            "description": description_text,
            "file_text": file_text,
        }
    }
