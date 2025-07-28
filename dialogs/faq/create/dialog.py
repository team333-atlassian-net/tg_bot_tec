import io
import logging
import pandas as pd

from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Row

from states import AddFAQSG
from dialogs.faq.create.handlers import *
from dialogs.faq.create.getters import *


logger = logging.getLogger(__name__)


method_window = Window(
    Const("Как вы хотите добавить вопрос?"),
    Row(
        Button(Const("📄 Excel"), id="excel", on_click=on_excel_chosen),
        Button(Const("✍️ Вручную"), id="manual", on_click=on_manual_chosen),
    ),
    Cancel(Const("❌ Отмена")),
    state=AddFAQSG.method,
)

question_window = Window(
    Const("Введите вопрос:"),
    MessageInput(on_question_entered),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=AddFAQSG.question,
)

answer_window = Window(
    Const("Введите ответ:"),
    MessageInput(on_answer_entered),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=AddFAQSG.answer,
)

category_window = Window(
    Const("Введите категорию (или напишите 'нет'):"),
    MessageInput(on_category_entered),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=AddFAQSG.category,
)

keywords_window = Window(
    Const("Введите ключевые слова через запятую:"),
    MessageInput(on_keywords_entered),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=AddFAQSG.keywords,
)

confirm_window = Window(
    Format(
        "❓ Вопрос: {dialog_data[question]}\n"
        "💬 Ответ: {dialog_data[answer]}\n"
        "🏷 Категория: {dialog_data[category]}\n"
        "🔍 Ключевые слова: {dialog_data[keywords]}"
    ),
    Row(
        Button(Const("✅ Сохранить"), id="confirm", on_click=on_manual_confirm),
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    getter=get_confirm_data,
    state=AddFAQSG.confirm,
)

upload_excel_window = Window(
    Const(
        "📄 Пришлите Excel-файл (.xlsx) с колонками: question, answer, keywords, category (опц.)"
    ),
    MessageInput(on_excel_uploaded, content_types=["document"]),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(AddFAQSG.method),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=AddFAQSG.upload_excel,
)

dialog = Dialog(
    method_window,
    question_window,
    answer_window,
    category_window,
    keywords_window,
    confirm_window,
    upload_excel_window,
)
