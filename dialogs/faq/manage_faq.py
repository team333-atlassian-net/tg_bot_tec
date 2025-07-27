import logging
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Button, Cancel, Row, Radio, ScrollingGroup
)
from dao.faq import delete_faq, get_all_faq, get_faq_by_id, update_faq, update_key_words

logger = logging.getLogger(__name__)

class ManageFAQSQ(StatesGroup):
    """Состояния для управления FAQ"""
    list = State()
    faq_action = State()
    edit_question = State()
    edit_answer = State()
    edit_category = State()
    edit_keywords = State()


# --- Геттеры ---

async def get_faq_list(dialog_manager: DialogManager, **kwargs):
    """
    Получение списка всех вопросов для отображения в списке.
    Возвращает список кортежей (вопрос, id).
    """
    faq = await get_all_faq()
    return {"faq": [(f.question, str(f.id)) for f in faq]}


async def get_faq_details(dialog_manager: DialogManager, **kwargs):
    """
    Получение подробной информации по выбранному вопросу.
    Если вопрос не найден, возвращает значения по умолчанию.
    Форматирует ключевые слова в строку.
    """
    faq_id = dialog_manager.dialog_data.get("faq_id")
    if not faq_id:
        return {
            "faq_question": "Неизвестный вопрос",
            "faq_answer": "",
            "faq_category": "Не указана",
            "faq_keywords": "",
        }
    faq = await get_faq_by_id(int(faq_id))
    if not faq:
        return {
            "faq_question": "Вопрос не найден",
            "faq_answer": "",
            "faq_category": "Не указана",
            "faq_keywords": "",
        }
    keywords_str = ", ".join(kw.word for kw in faq.keywords) if faq.keywords else "-"
    return {
        "faq_question": faq.question,
        "faq_answer": faq.answer,
        "faq_category": faq.category or "-",
        "faq_keywords": keywords_str,
    }


# --- Коллбэки ---

async def on_faq_selected(callback: CallbackQuery, widget, manager: DialogManager, item_id: str):
    """
    Обработчик выбора вопроса из списка.
    Сохраняет ID выбранного вопроса и переключается на окно действий.
    """
    manager.dialog_data["faq_id"] = item_id
    await manager.switch_to(ManageFAQSQ.faq_action)


async def on_edit_question_start(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """Переход в состояние редактирования вопроса."""
    await dialog_manager.switch_to(ManageFAQSQ.edit_question)


async def on_edit_answer_start(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """Переход в состояние редактирования ответа."""
    await dialog_manager.switch_to(ManageFAQSQ.edit_answer)


async def on_edit_question(message: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Сохраняет отредактированный вопрос в базу.
    Логирует действие администратора.
    Отправляет подтверждение и завершает диалог.
    """
    faq_id = dialog_manager.dialog_data.get("faq_id")
    if faq_id:
        await update_faq(int(faq_id), value.get_value(), None, None)
        await message.answer("✏️ Вопрос обновлен.")
        logger.info("Админ обновил вопрос (/manage_faq)")
        await dialog_manager.switch_to(ManageFAQSQ.faq_action)
    await dialog_manager.done()


async def on_edit_answer(message: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Сохраняет отредактированный ответ в базу.
    Логирует действие администратора.
    Отправляет подтверждение и завершает диалог.
    """
    faq_id = dialog_manager.dialog_data.get("faq_id")
    if faq_id:
        await update_faq(int(faq_id), None, value.get_value(), None)
        await message.answer("📝 Описание обновлено.")
        logger.info("Админ обновил ответ (/manage_faq)")
        await dialog_manager.switch_to(ManageFAQSQ.faq_action)
    await dialog_manager.done()


async def on_edit_category(msg: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Сохраняет обновленную категорию вопроса.
    Логирует действие администратора.
    Отправляет подтверждение и завершает диалог.
    """
    faq_id = dialog_manager.dialog_data.get("faq_id")
    if faq_id:
        await update_faq(int(faq_id), None, None, new_category=value.get_value())
        await msg.answer("🏷 Категория обновлена.")
        logger.info("Админ обновил категорию вопроса (/manage_faq)")
        await dialog_manager.switch_to(ManageFAQSQ.faq_action)
    await dialog_manager.done()


async def on_edit_keywords(msg: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Обновляет ключевые слова вопроса.
    Разбивает строку ключевых слов по запятым.
    Логирует действие администратора.
    Отправляет подтверждение и завершает диалог.
    """
    faq_id = dialog_manager.dialog_data.get("faq_id")
    if faq_id:
        words = [w.strip() for w in value.get_value().split(",") if w.strip()]
        await update_key_words(int(faq_id), keywords=words)
        await msg.answer("🔑 Ключевые слова обновлены.")
        await dialog_manager.switch_to(ManageFAQSQ.faq_action)
        logger.info("Админ обновил ключевые слова вопроса (/manage_faq)")
    await dialog_manager.done()


async def on_delete_faq(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Удаляет выбранный вопрос из базы.
    Отправляет подтверждение и логирует действие администратора.
    Завершает диалог.
    """
    faq_id = dialog_manager.dialog_data.get("faq_id")
    if faq_id:
        await delete_faq(int(faq_id))
        await callback.message.answer("✅ Вопрос удален.")
        logger.info("Администратор удалил мероприятие (/manage_faqs)")
        await dialog_manager.switch_to(ManageFAQSQ.list)
    await dialog_manager.done()


async def on_exit(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Выход из режима редактирования FAQ.
    Отправляет сообщение пользователю и завершает диалог.
    """
    await callback.message.answer("❌ Вы вышли из режима редактирования.")
    await dialog_manager.done()

# --- Окна ---

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
    Cancel(Const("❌ Выйти из режима редактирования"), id="exit_editing", on_click=on_exit),
    state=ManageFAQSQ.list,
    getter=get_faq_list,
)

faq_detail_window = Window(
    Const("Выберите действие с вопросом:"),
    Format("<b>{faq_question}</b>"),
    Format("Ответ: {faq_answer}\nКатегория: {faq_category}\nКлючевые слова: {faq_keywords}"),
    Row(
        Button(Const("✏️ Вопрос"), id="edit_question", on_click=on_edit_question_start),
        Button(Const("✏️ Ответ"), id="edit_desc", on_click=on_edit_answer_start),
    ),
    Row(
        Button(Const("✏️ Категория"), id="edit_category",
               on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.edit_category),),
        Button(Const("✏️ Ключевые слова"), id="edit_keywords",
               on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.edit_keywords),
               ),
    ),
    Button(Const("🗑 Удалить"), id="delete", on_click=on_delete_faq),
    Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.list)),
    state=ManageFAQSQ.faq_action,
    getter=get_faq_details,
)

edit_question_window = Window(
    Const("Редактирование вопроса:"),
    Format("Вы хотите изменить вопрос: \n<b>{faq_question}</b>"),
    TextInput("edit_question", on_success=on_edit_question),
    Row(
        Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.faq_action)),
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
        Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.faq_action)),
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
        Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.faq_action)),
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
        Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageFAQSQ.faq_action)),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageFAQSQ.edit_keywords,
    getter=get_faq_details,
)

manage_faq_dialog = Dialog(
    list_window,
    faq_detail_window,
    edit_question_window,
    edit_answer_window,
    edit_category_window,
    edit_keywords_window
)
