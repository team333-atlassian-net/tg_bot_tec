import logging

from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Row, Radio, ScrollingGroup

from states import FAQViewSG
from dialogs.faq.view.handlers import *
from dialogs.faq.view.getters import *

logger = logging.getLogger(__name__)


# Главное меню
faq_menu_window = Window(
    Const("📚 Что вы хотите сделать?"),
    Button(
        Const("📋 Посмотреть все вопросы"),
        id="all",
        on_click=lambda c, b, m: m.switch_to(FAQViewSG.list_all),
    ),
    Button(
        Const("🏷 Посмотреть все категории вопросов"),
        id="by_cat",
        on_click=lambda c, b, m: m.switch_to(FAQViewSG.category_select),
    ),
    Cancel(Const("❌ Отмена")),
    state=FAQViewSG.menu,
)

# Список всех вопросов
faq_list_window = Window(
    Const("📋 Все вопросы:"),
    ScrollingGroup(
        Radio(
            Format("{item[1]}"),
            Format("{item[1]}"),
            id="faq_radio",
            items="faqs",
            item_id_getter=lambda x: x[0],
            on_click=on_faq_selected,
        ),
        id="faq_scroll",
        width=1,
        height=5,
    ),
    Back(Const("⬅️ Назад")),
    state=FAQViewSG.list_all,
    getter=get_faq_list,
)

# Список всех категорий
faq_category_select_window = Window(
    Const("📋 Выберите категорию:"),
    ScrollingGroup(
        Radio(
            Format("{item}"),
            Format("{item}"),
            id="cat_radio",
            items="categories",
            item_id_getter=lambda x: x,
            on_click=on_category_selected,
        ),
        id="cat_scroll",
        width=1,
        height=5,
    ),
    Button(Const("⬅️ Назад"), id="back_to_menu_from_cat", on_click=on_back_to_menu),
    state=FAQViewSG.category_select,
    getter=get_category_list,
)

# Список вопросов по категории
faq_by_category_window = Window(
    Format("📂 Вопросы по категории: <b>{category}</b>"),
    ScrollingGroup(
        Radio(
            Format("{item[1]}"),
            Format("{item[1]}"),
            id="faq_cat_radio",
            items="faqs",
            item_id_getter=lambda x: x[0],
            on_click=on_faq_selected,
        ),
        id="faq_cat_scroll",
        width=1,
        height=5,
    ),
    Back(Const("⬅️ Назад")),
    state=FAQViewSG.category_questions,
    getter=get_faqs_by_category,
)

# Детали вопроса
faq_detail_window = Window(
    Format("📌 <b>{faq.question}</b>\n\n{faq.answer}"),
    Row(
        Button(Const("⬅️ Назад"), id="back_from_detail", on_click=on_detail_back),
        Cancel(Const("❌ Закрыть")),
    ),
    state=FAQViewSG.detail,
    getter=detail_window_getter,
)

dialog = Dialog(
    faq_menu_window,
    faq_list_window,
    faq_category_select_window,
    faq_by_category_window,
    faq_detail_window,
)
