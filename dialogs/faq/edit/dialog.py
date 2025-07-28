import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Radio, ScrollingGroup
from states import ManageFAQSQ
from dialogs.faq.edit.handlers import *
from dialogs.faq.edit.getters import *

logger = logging.getLogger(__name__)


list_window = Window(
    Const("📋 Список вопросов:"),
    ScrollingGroup(
        Radio(
            checked_text=Format("✏️ {item[0]}"),
            unchecked_text=Format("✏️ {item[0]}"),
            id="faq_radio",
            item_id_getter=lambda x: x[1],
            items="faq",
            on_click=on_faq_selected,
        ),
        id="faq_scroll",
        width=1,
        height=5,
    ),
    Cancel(
        Const("❌ Выйти из режима редактирования"), id="exit_editing", on_click=on_exit
    ),
    state=ManageFAQSQ.list,
    getter=get_faq_list,
)

faq_detail_window = Window(
    Const("Выберите действие с вопросом:"),
    Format("<b>{faq_question}</b>"),
    Format(
        "Ответ: {faq_answer}\nКатегория: {faq_category}\nКлючевые слова: {faq_keywords}"
    ),
    Row(
        Button(Const("✏️ Вопрос"), id="edit_question", on_click=on_edit_question_start),
        Button(Const("✏️ Ответ"), id="edit_desc", on_click=on_edit_answer_start),
    ),
    Row(
        Button(
            Const("✏️ Категория"),
            id="edit_category",
            on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.edit_category),
        ),
        Button(
            Const("✏️ Ключевые слова"),
            id="edit_keywords",
            on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.edit_keywords),
        ),
    ),
    Button(Const("🗑 Удалить"), id="delete", on_click=on_delete_faq),
    Button(
        Const("⬅️ Назад"),
        id="back",
        on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.list),
    ),
    state=ManageFAQSQ.faq_action,
    getter=get_faq_details,
)

edit_question_window = Window(
    Const("Редактирование вопроса:"),
    Format("Вы хотите изменить вопрос: \n<b>{faq_question}</b>"),
    TextInput("edit_question", on_success=on_edit_question),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.faq_action),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageFAQSQ.edit_question,
    getter=get_faq_details,
)

edit_answer_window = Window(
    Const("Редактирование ответа на вопрос:"),
    Format("<b>{faq_question}</b>"),
    Format("Вы хотите изменить ответ: \n{faq_answer}"),
    TextInput("edit_desc", on_success=on_edit_answer),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.faq_action),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageFAQSQ.edit_answer,
    getter=get_faq_details,
)

edit_category_window = Window(
    Const("Редактирование категории:"),
    Format("Текущая категория: {faq_category}"),
    TextInput("edit_category", on_success=on_edit_category),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.faq_action),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageFAQSQ.edit_category,
    getter=get_faq_details,
)

edit_keywords_window = Window(
    Const("Редактирование ключевых слов:"),
    Format("Текущие ключевые слова: {faq_keywords}\n\nВведите новые через запятую:"),
    TextInput("edit_keywords", on_success=on_edit_keywords),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.faq_action),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageFAQSQ.edit_keywords,
    getter=get_faq_details,
)

dialog = Dialog(
    list_window,
    faq_detail_window,
    edit_question_window,
    edit_answer_window,
    edit_category_window,
    edit_keywords_window,
)
