import logging

from aiogram_dialog import DialogManager

logger = logging.getLogger(__name__)


async def get_search_results(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для окна с результатами поиска.
    """
    return {
        "faqs": dialog_manager.dialog_data.get("search_results", []),
        "query": dialog_manager.dialog_data.get("query", ""),
    }
