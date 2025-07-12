import logging
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Button, Cancel, Row, Radio, ScrollingGroup
)

from dao.events import get_all_events, get_event_by_id, delete_event, update_event

logger = logging.getLogger(__name__)


# --- Состояния ---

class ManageEventSG(StatesGroup):
    list = State()
    event_action = State()
    edit_title = State()
    edit_description = State()


# --- Геттеры ---

async def get_event_list(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает список всех мероприятий.
    """
    events = await get_all_events()
    return {"events": [(e.title, str(e.id)) for e in events]}


async def get_event_details(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает детали выбранного мероприятия.
    """
    event_id = dialog_manager.dialog_data.get("event_id")
    if not event_id:
        return {"event_title": "Неизвестное мероприятие", "event_description": ""}
    event = await get_event_by_id(int(event_id))
    if not event:
        return {"event_title": "Мероприятие не найдено", "event_description": ""}
    return {
        "event_title": event.title,
        "event_description": event.description,
    }


# --- Коллбэки ---

async def on_event_selected(callback: CallbackQuery, widget, manager: DialogManager, item_id: str):
    """
    Сохраняет выбранное мероприятие и переключается на детали.
    """
    manager.dialog_data["event_id"] = item_id
    await manager.switch_to(ManageEventSG.event_action)


async def on_edit_title_start(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Переход к окну редактирования названия.
    """
    await dialog_manager.switch_to(ManageEventSG.edit_title)


async def on_edit_description_start(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Переход к окну редактирования описания.
    """
    await dialog_manager.switch_to(ManageEventSG.edit_description)


async def on_edit_title(message: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Сохраняет новое название мероприятия и завершает диалог.
    """
    event_id = dialog_manager.dialog_data.get("event_id")
    if event_id:
        await update_event(int(event_id), value.get_value(), None)
        await message.answer("✏️ Название обновлено.")
        logger.info("Админ обновил название (/manage_events)")
    await dialog_manager.done()


async def on_edit_description(message: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Сохраняет новое описание мероприятия и завершает диалог.
    """
    event_id = dialog_manager.dialog_data.get("event_id")
    if event_id:
        await update_event(int(event_id), None, value.get_value())
        await message.answer("📝 Описание обновлено.")
        logger.info("Админ обновил описание (/manage_events)")
    await dialog_manager.done()


async def on_delete_event(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Удаляет выбранное мероприятие.
    """
    event_id = dialog_manager.dialog_data.get("event_id")
    if event_id:
        await delete_event(int(event_id))
        await callback.message.answer("✅ Мероприятие удалено.")
        logger.info("Администратор удалил мероприятие (/manage_events)")
    await dialog_manager.done()


async def on_exit(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Выход из режима редактирования.
    """
    await callback.message.answer("❌ Вы вышли из режима редактирования.")
    await dialog_manager.done()


# --- Окна ---

list_window = Window(
    Const("📋 Список мероприятий:"),
    ScrollingGroup(
        Radio(
            checked_text=Format("✏️ {item[0]}"),
            unchecked_text=Format("✏️ {item[0]}"),
            id="event_radio",
            item_id_getter=lambda x: x[1],
            items="events",
            on_click=on_event_selected,
        ),
        id="event_scroll",
        width=1,
        height=3,
    ),
    Cancel(Const("❌ Выйти из режима редактирования"), id="exit_editing", on_click=on_exit),
    state=ManageEventSG.list,
    getter=get_event_list,
)

event_detail_window = Window(
    Const("Выберите действие с мероприятием:"),
    Format("<b>{event_title}</b>"),
    Format("{event_description}"),
    Row(
        Button(Const("✏️ Название"), id="edit_title", on_click=on_edit_title_start),
        Button(Const("✏️ Описание"), id="edit_desc", on_click=on_edit_description_start),
        Button(Const("🗑 Удалить"), id="delete", on_click=on_delete_event),
    ),
    Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageEventSG.list)),
    state=ManageEventSG.event_action,
    getter=get_event_details,
)

edit_title_window = Window(
    Const("Редактирование названия мероприятия:"),
    Format("Вы хотите изменить название: \n<b>{event_title}</b>"),
    TextInput("edit_title", on_success=on_edit_title),
    Cancel(Const("❌ Отмена")),
    state=ManageEventSG.edit_title,
    getter=get_event_details,
)


edit_description_window = Window(
    Const("Редактирование описания мероприятия:"),
    Format("<b>{event_title}</b>"),
    Format("Вы хотите изменить описание: \n{event_description}"),
    TextInput("edit_desc", on_success=on_edit_description),
    Cancel(Const("❌ Отмена")),
    state=ManageEventSG.edit_description,
    getter=get_event_details,
)


manage_event_dialog = Dialog(
    list_window,
    event_detail_window,
    edit_title_window,
    edit_description_window,
)