import logging

from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Select, Radio, ScrollingGroup

from dao.faq import search_faq
from dialogs.faq.view_faq import detail_window_getter

logger = logging.getLogger(__name__)

class FAQSearchSG(StatesGroup):
    """
    Состояния для диалога поиска FAQ
    """
    search_input = State()
    search_results = State()
    detail = State()

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
    dialog_manager.dialog_data["search_results"] = [(str(f.id), f.question) for f in faqs]
    dialog_manager.dialog_data["query"] = query
    logger.info(f"Пользователь выполнил поиск FAQ по запросу: '{query}' (/search_faq)")
    await dialog_manager.switch_to(FAQSearchSG.search_results)

async def get_search_results(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для окна с результатами поиска.
    """
    return {
        "faqs": dialog_manager.dialog_data.get("search_results", []),
        "query": dialog_manager.dialog_data.get("query", "")
    }

async def on_search_result_selected(callback, widget: Select, manager: DialogManager, selected_id: str):
    """
    Обработка выбора результата поиска.
    Действия:
        - Сохраняет ID выбранного вопроса
        - Переходит к состоянию показа подробностей вопроса
    """
    manager.dialog_data["selected_faq_id"] = int(selected_id)
    await manager.switch_to(FAQSearchSG.detail)

# --- Окна ---

# Окно ввода поискового запроса
search_input_window = Window(
    Const("🔍 Введите ключевое слово или фразу для поиска FAQ:"),
    MessageInput(on_search_input),
    Cancel(Const("❌ Отмена")),
    state=FAQSearchSG.search_input,
)

# Окно с результатами поиска
search_results_window = Window(
    Format("🔎 Результаты по запросу: <b>{query}</b>"),
    ScrollingGroup(
        Radio(
            Format("{item[1]}"),
            Format("{item[1]}"),
            id="search_results_radio",
            items="faqs",
            item_id_getter=lambda x: x[0],
            on_click=on_search_result_selected,
        ),
        id="search_scroll",
        width=1,
        height=5,
    ),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    getter=get_search_results,
    state=FAQSearchSG.search_results,
)

# Окно с деталями выбранного FAQ
search_faq_detail_window = Window(
    Format("📌 <b>{faq.question}</b>\n\n{faq.answer}"),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Закрыть"))
    ),
    state=FAQSearchSG.detail,
    getter=detail_window_getter,  # переиспользуется из view_faq
)

faq_search_dialog = Dialog(
    search_input_window,
    search_results_window,
    search_faq_detail_window,
)
