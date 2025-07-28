import logging

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from dao.faq import search_faq
from states import FAQSearchSG


logger = logging.getLogger(__name__)


async def on_search_input(message: Message, widget, dialog_manager: DialogManager):
    """
    Обработка ввода поискового запроса пользователем.
    Действия:
        - Проверяет, что запрос не пустой и является текстом
        - Выполняет поиск FAQ по запросу
        - Сохраняет результаты и запрос в dialog_data
        - Переходит к состоянию отображения результатов поиска
    """
    query = message.text
    if not query or not query.strip():
        await message.answer("❗ Введите поисковый запрос.")
        return
    query = query.strip()
    faqs = await search_faq(query)
    dialog_manager.dialog_data["search_results"] = [
        (str(f.id), f.question) for f in faqs
    ]
    dialog_manager.dialog_data["query"] = query
    logger.info(f"Пользователь выполнил поиск FAQ по запросу: '{query}' (/search_faq)")
    await dialog_manager.switch_to(FAQSearchSG.search_results)


async def on_search_result_selected(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    """
    Обработка выбора результата поиска.
    Действия:
        - Сохраняет ID выбранного вопроса
        - Переходит к состоянию показа подробностей вопроса
    """
    manager.dialog_data["selected_faq_id"] = int(selected_id)
    await manager.switch_to(FAQSearchSG.detail)
