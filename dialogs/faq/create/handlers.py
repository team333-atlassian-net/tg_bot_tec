import io
import logging
import pandas as pd

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window, DialogManager

from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Row

from dao.faq import add_faq_with_keywords
from utils.auth import require_admin
from states import AddFAQSG

logger = logging.getLogger(__name__)


# --- Обработчики ручного ввода ---


async def on_manual_chosen(callback: CallbackQuery, button, manager: DialogManager):
    """
    Обработчик выбора ручного ввода FAQ.
    Переключает состояние на ввод вопроса.
    """
    await manager.switch_to(AddFAQSG.question)


async def on_question_entered(
    message: Message, widget: TextInput, dialog_manager: DialogManager
):
    """
    Обработчик ввода вопроса.
    Сохраняет вопрос в dialog_data и переходит к вводу ответа.
    """
    dialog_manager.dialog_data["question"] = message.text
    await dialog_manager.switch_to(AddFAQSG.answer)


async def on_answer_entered(
    message: Message, widget: TextInput, dialog_manager: DialogManager
):
    """
    Обработчик ввода ответа.
    Сохраняет ответ в dialog_data и переходит к вводу категории.
    """
    dialog_manager.dialog_data["answer"] = message.text
    await dialog_manager.switch_to(AddFAQSG.category)


async def on_category_entered(
    message: Message, widget: TextInput, dialog_manager: DialogManager
):
    """
    Обработчик ввода категории.
    Преобразует ввод в нижний регистр, если введено 'нет' или 'пропустить',
    категория считается пустой (None).
    Иначе сохраняет введенную категорию и переходит к вводу ключевых слов.
    """
    text = message.text.strip().lower()
    dialog_manager.dialog_data["category"] = (
        "-" if text in ("нет", "пропустить") else message.text
    )
    await dialog_manager.switch_to(AddFAQSG.keywords)


async def on_keywords_entered(
    message: Message, widget: TextInput, dialog_manager: DialogManager
):
    """
    Обработчик ввода ключевых слов.
    Разбивает строку по запятым, очищает пробелы и сохраняет список ключевых слов.
    Переходит к подтверждению данных.
    """
    keywords = [kw.strip() for kw in message.text.split(",") if kw.strip()]
    dialog_manager.dialog_data["keywords"] = keywords
    await dialog_manager.switch_to(AddFAQSG.confirm)


async def on_manual_confirm(
    callback: CallbackQuery, widget, dialog_manager: DialogManager
):
    """
    Обработчик подтверждения сохранения вручную введенного FAQ.
    Добавляет вопрос с ключевыми словами в базу данных.
    Отправляет пользователю сообщение об успешном добавлении.
    Завершает диалог.
    """
    data = dialog_manager.dialog_data
    if data["category"] == "-":
        data["category"] = None
    await add_faq_with_keywords(
        question=data["question"],
        answer=data["answer"],
        category=data["category"],
        keywords=data["keywords"],
    )
    await callback.message.answer("✅ Вопрос успешно добавлен.")
    logger.info("Администратор добавил вопрос (faq) в БД (/add_faq)")
    await dialog_manager.done()


# --- Обработчики Excel загрузки ---


async def on_excel_chosen(callback: CallbackQuery, button, manager: DialogManager):
    """
    Обработчик выбора способа добавления через Excel.
    Переключает состояние на загрузку Excel файла.
    """
    await manager.switch_to(AddFAQSG.upload_excel)


async def on_excel_uploaded(message: Message, widget, dialog_manager: DialogManager):
    """
    Обработчик загрузки Excel файла.
    Проверяет права администратора.
    Проверяет формат файла (.xlsx).
    Считывает Excel и проверяет необходимые колонки.
    Проходит по каждой строке и добавляет FAQ с ключевыми словами.
    Отправляет сообщение с количеством успешно добавленных записей.
    Завершает диалог.
    """
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
        await message.answer(
            "❌ В Excel-файле должны быть колонки: question, answer, keywords (через запятую)"
        )
        return

    count = 0
    for _, row in df.iterrows():
        keywords = [kw.strip() for kw in str(row["keywords"]).split(",") if kw.strip()]
        await add_faq_with_keywords(
            question=row["question"],
            answer=row["answer"],
            category=row.get("category"),
            keywords=keywords,
        )
        count += 1

    await message.answer(f"✅ Загружено {count} FAQ из Excel.")
    logger.info(f"Админ загрузин {count} 10 faq из excel файла (/add_faq)")
    await dialog_manager.done()
