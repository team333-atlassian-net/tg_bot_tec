import logging

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput

from dao.events import delete_event, update_event
from states import ManageEventSG

logger = logging.getLogger(__name__)


async def on_event_selected(
    callback: CallbackQuery, widget, manager: DialogManager, item_id: str
):
    """
    Сохраняет выбранное мероприятие и переключается на детали.
    """
    manager.dialog_data["event_id"] = item_id
    await manager.switch_to(ManageEventSG.event_action)


async def on_edit_title_start(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Переход к окну редактирования названия.
    """
    await dialog_manager.switch_to(ManageEventSG.edit_title)


async def on_edit_description_start(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Переход к окну редактирования описания.
    """
    await dialog_manager.switch_to(ManageEventSG.edit_description)


async def on_edit_title(
    message: Message, value: TextInput, dialog_manager: DialogManager, widget
):
    """
    Сохраняет новое название мероприятия и завершает диалог.
    """
    event_id = dialog_manager.dialog_data.get("event_id")
    if event_id:
        await update_event(int(event_id), value.get_value(), None)
        await message.answer("✏️ Название обновлено.")
        logger.info("Админ обновил название (/manage_events)")
        await dialog_manager.switch_to(ManageEventSG.event_action)
    await dialog_manager.done()


async def on_edit_description(
    message: Message, value: TextInput, dialog_manager: DialogManager, widget
):
    """
    Сохраняет новое описание мероприятия и завершает диалог.
    """
    event_id = dialog_manager.dialog_data.get("event_id")
    if event_id:
        await update_event(int(event_id), None, value.get_value())
        await message.answer("📝 Описание обновлено.")
        logger.info("Админ обновил описание (/manage_events)")
        await dialog_manager.switch_to(ManageEventSG.event_action)
    await dialog_manager.done()


async def on_delete_event(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Удаляет выбранное мероприятие.
    """
    event_id = dialog_manager.dialog_data.get("event_id")
    if event_id:
        await delete_event(int(event_id))
        await callback.message.answer("✅ Мероприятие удалено.")
        logger.info("Администратор удалил мероприятие (/manage_events)")
        await dialog_manager.switch_to(ManageEventSG.list)
    await dialog_manager.done()


async def on_exit(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    """
    Выход из режима редактирования.
    """
    await callback.message.answer("❌ Вы вышли из режима редактирования.")
    await dialog_manager.done()
