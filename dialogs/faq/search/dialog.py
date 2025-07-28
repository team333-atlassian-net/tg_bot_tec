import logging

from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Radio, ScrollingGroup

from dialogs.faq.view.getters import detail_window_getter
from states import FAQSearchSG
from dialogs.faq.search.handlers import *
from dialogs.faq.search.getters import *

logger = logging.getLogger(__name__)

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
    Row(Back(Const("⬅️ Назад")), Cancel(Const("❌ Закрыть"))),
    state=FAQSearchSG.detail,
    getter=detail_window_getter,  # переиспользуется из view_faq
)

dialog = Dialog(
    search_input_window,
    search_results_window,
    search_faq_detail_window,
)
