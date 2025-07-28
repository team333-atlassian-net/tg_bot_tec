import logging
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from dao.faq import delete_faq, update_faq, update_key_words
from states import ManageFAQSQ


logger = logging.getLogger(__name__)


async def on_faq_selected(
    callback: CallbackQuery, widget, manager: DialogManager, item_id: str
):
    """
    Обработчик выбора вопроса из списка.
    Сохраняет ID выбранного вопроса и переключается на окно действий.
    """
    manager.dialog_data["faq_id"] = item_id
    await manager.switch_to(ManageFAQSQ.faq_action)


async def on_edit_question_start(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """Переход в состояние редактирования вопроса."""
    await dialog_manager.switch_to(ManageFAQSQ.edit_question)


async def on_edit_answer_start(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """Переход в состояние редактирования ответа."""
    await dialog_manager.switch_to(ManageFAQSQ.edit_answer)


async def on_edit_question(
    message: Message, value: TextInput, dialog_manager: DialogManager, widget
):
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


async def on_edit_answer(
    message: Message, value: TextInput, dialog_manager: DialogManager, widget
):
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


async def on_edit_category(
    msg: Message, value: TextInput, dialog_manager: DialogManager, widget
):
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


async def on_edit_keywords(
    msg: Message, value: TextInput, dialog_manager: DialogManager, widget
):
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


async def on_delete_faq(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
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


async def on_exit(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Выход из режима редактирования FAQ.
    Отправляет сообщение пользователю и завершает диалог.
    """
    await callback.message.answer("❌ Вы вышли из режима редактирования.")
    await dialog_manager.done()
