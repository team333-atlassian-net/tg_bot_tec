import io
import logging
import pandas as pd

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Row

from dao.faq import add_faq_with_keywords
from utils.auth import require_admin


logger = logging.getLogger(__name__)


class AddFAQSG(StatesGroup):
    method = State()
    question = State()
    answer = State()
    category = State()
    keywords = State()
    confirm = State()
    upload_excel = State()

# --- Обработчики ручного ввода ---

async def on_manual_chosen(callback: CallbackQuery, button, manager: DialogManager):
    await manager.switch_to(AddFAQSG.question)

async def on_question_entered(message: Message, widget: TextInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["question"] = message.text
    await dialog_manager.switch_to(AddFAQSG.answer)

async def on_answer_entered(message: Message, widget: TextInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["answer"] = message.text
    await dialog_manager.switch_to(AddFAQSG.category)

async def on_category_entered(message: Message, widget: TextInput, dialog_manager: DialogManager):
    text = message.text.strip().lower()
    dialog_manager.dialog_data["category"] = None if text in ("нет", "пропустить") else message.text
    await dialog_manager.switch_to(AddFAQSG.keywords)

async def on_keywords_entered(message: Message, widget: TextInput, dialog_manager: DialogManager):
    keywords = [kw.strip() for kw in message.text.split(",") if kw.strip()]
    dialog_manager.dialog_data["keywords"] = keywords
    await dialog_manager.switch_to(AddFAQSG.confirm)

async def get_confirm_data(dialog_manager: DialogManager, **kwargs):
    return {
        "dialog_data": dialog_manager.dialog_data,
    }

async def on_manual_confirm(callback: CallbackQuery, widget, dialog_manager: DialogManager):
    data = dialog_manager.dialog_data
    await add_faq_with_keywords(
        question=data["question"],
        answer=data["answer"],
        category=data["category"],
        keywords=data["keywords"]
    )
    await callback.message.answer("✅ Вопрос успешно добавлен.")
    await dialog_manager.done()


# --- Обработчики Excel ---
async def on_excel_chosen(callback: CallbackQuery, button, manager: DialogManager):
    await manager.switch_to(AddFAQSG.upload_excel)

async def on_excel_uploaded(message: Message, widget, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return

    file = message.document
    if not file.file_name.endswith(".xlsx"):
        await message.answer("❌ Пожалуйста, отправьте Excel-файл (.xlsx)")
        return

    file_bytes = await message.bot.download(file)
    df = pd.read_excel(io.BytesIO(file_bytes.read()))
    required_columns = {"question", "answer", "keywords"}

    if not required_columns.issubset(df.columns):
        await message.answer("❌ В Excel-файле должны быть колонки: question, answer, keywords (через запятую)")
        return

    count = 0
    for _, row in df.iterrows():
        keywords = [kw.strip() for kw in str(row["keywords"]).split(",") if kw.strip()]
        await add_faq_with_keywords(
            question=row["question"],
            answer=row["answer"],
            category=row.get("category"),
            keywords=keywords
        )
        count += 1

    await message.answer(f"✅ Загружено {count} FAQ из Excel.")
    await dialog_manager.done()


# --- Окна ---

method_window = Window(
    Const("Как вы хотите добавить вопрос?"),
    Row(
        Button(Const("📄 Excel"), id="excel", on_click=on_excel_chosen),
        Button(Const("✍️ Вручную"), id="manual", on_click=on_manual_chosen),
    ),
    Cancel(Const("❌ Отмена")),
    state=AddFAQSG.method,
)

question_window = Window(Const("Введите вопрос:"), MessageInput(on_question_entered), state=AddFAQSG.question)
answer_window = Window(Const("Введите ответ:"), MessageInput(on_answer_entered), state=AddFAQSG.answer)
category_window = Window(Const("Введите категорию (или напишите 'нет'):"), MessageInput(on_category_entered), state=AddFAQSG.category)
keywords_window = Window(Const("Введите ключевые слова через запятую:"), MessageInput(on_keywords_entered), state=AddFAQSG.keywords)

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
    Const("📄 Пришлите Excel-файл (.xlsx) с колонками: question, answer, keywords, category (опц.)"),
    MessageInput(on_excel_uploaded, content_types=["document"]),
    Cancel(Const("❌ Отмена")),
    state=AddFAQSG.upload_excel,
)

add_faq_dialog = Dialog(
    method_window,
    question_window,
    answer_window,
    category_window,
    keywords_window,
    confirm_window,
    upload_excel_window,
)
