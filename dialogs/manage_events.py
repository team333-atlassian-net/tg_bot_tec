import logging
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Radio, ScrollingGroup, Button, Row
from aiogram_dialog.widgets.input import TextInput
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from dao.events import delete_event, get_all_events, update_event, get_event_by_id 

logger = logging.getLogger(__name__)

class ManageEventSG(StatesGroup):
    """
    Состояния диалога для управления мероприятиями.
    """
    list = State()                # Просмотр списка мероприятий
    event_action = State()        # Выбор действия для конкретного мероприятия
    edit_title = State()          # Редактирование названия
    edit_description = State()    # Редактирование описания


async def get_event_list(dialog_manager: DialogManager, **kwargs) -> dict:
    """
    Получение списка мероприятий для отображения в диалоге
    """
    events = await get_all_events()
    # возвращает словарь с ключом "events" и списком кортежей (название, id).
    return {
        "events": [(e.title, str(e.id)) for e in events]
    }


async def get_event_details(dialog_manager: DialogManager, **kwargs) -> dict:
    """
    Получение деталей выбранного мероприятия (название и описание).
    Возвращает:

    dict: словарь с ключами "event_title" и "event_description".
            Если мероприятие не найдено, возвращаются сообщения об ошибке.
    """
    event_id = dialog_manager.dialog_data.get("event_id")
    if not event_id:
        return {"event_title": "Неизвестное мероприятие", "event_description": ""}
    event = await get_event_by_id(int(event_id))
    if not event:
        return {"event_title": "Мероприятие не найдено", "event_description": ""}
    return {
        "event_title": event.title,
        "event_description": event.description
    }


async def on_event_chosen(callback, widget, manager: DialogManager, item_id: str):
    """
    Обработчик выбора мероприятия из списка.
    Сохраняет выбранный event_id и переходит к состоянию выбора действия.
    """
    manager.dialog_data["event_id"] = item_id
    await manager.switch_to(ManageEventSG.event_action)


async def on_delete(callback, widget, dialog_manager: DialogManager, **kwargs):
    """
    Обработчик удаления выбранного мероприятия.
    Удаляет мероприятие из базы, отправляет сообщение и завершает диалог.
    """
    event_id = dialog_manager.dialog_data.get("event_id")
    if event_id:
        await delete_event(int(event_id))
        await callback.message.answer("✅ Мероприятие удалено.")
        logger.info("Администратор удалил мероприятие (/manage_events)")
    await dialog_manager.done()


async def on_edit_title_start(callback, widget, dialog_manager: DialogManager, **kwargs):
    """
    Обработчик начала редактирования названия мероприятия.
    Переключает состояние диалога на редактирование названия.
    """
    await dialog_manager.switch_to(ManageEventSG.edit_title)


async def on_edit_title(message: Message, value: str, dialog_manager: DialogManager, widget):
    """
    Обработчик ввода нового названия мероприятия.
    Сохраняет новое название и переключает состояние на редактирование описания.
    """
    dialog_manager.dialog_data["new_title"] = value.get_value()
    await dialog_manager.switch_to(ManageEventSG.edit_description)


async def on_edit_description(message: Message, value: str, dialog_manager: DialogManager, widget):
    """
    Обработчик ввода нового описания мероприятия.
    Обновляет данные мероприятия в базе, сообщает об успехе и завершает диалог.
    """
    new_description = value.get_value()
    new_title = dialog_manager.dialog_data.get("new_title")
    event_id = dialog_manager.dialog_data.get("event_id")
    if event_id and new_title:
        await update_event(int(event_id), new_title, new_description)
        await message.answer("✏️ Мероприятие отредактировано.")
        logger.info("Администратор отредактировал мероприятие (/manage_events)")
    await dialog_manager.done()


async def on_exit_editing(callback, widget, dialog_manager: DialogManager, **kwargs):
    """
    Обработчик выхода из режима редактирования.
    Завершает диалог и отправляет уведомление пользователю.
    """
    await dialog_manager.done()
    await callback.message.answer("❌ Вы вышли из режима редактирования.")
    

manage_event_dialog = Dialog(
    Window(
        Const("📋 Список мероприятий:"),
        ScrollingGroup(
            Radio(
                Format("✏️ {item[0]}"),    # текст для выбранной кнопки
                Format("✏️ {item[0]}"),    # текст для невыбранной кнопки
                id="event_radio",
                item_id_getter=lambda x: x[1],
                on_click=on_event_chosen,
                items="events",
            ),
            id="event_scroll",
            width=1,
            height=3,
        ),
        Button(Const("❌ Выйти из режима редактирования"), id="exit_editing", on_click=on_exit_editing),
        state=ManageEventSG.list,
        getter=get_event_list,
    ),
    Window(
        Const("Выберите действие с мероприятием:"),
        Format("<b>{event_title}</b>"),
        Format("{event_description}"),
        Row(
            Button(Const("✏️ Редактировать"), id="edit", on_click=on_edit_title_start),
            Button(Const("🗑 Удалить"), id="delete", on_click=on_delete),
        ),
        Button(Const("⬅️ Назад к списку"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageEventSG.list)),
        state=ManageEventSG.event_action,
        getter=get_event_details,
    ),
    Window(
        Const("Введите новое название мероприятия:"),
        TextInput("edit_title", on_success=on_edit_title),
        state=ManageEventSG.edit_title,
    ),
    Window(
        Const("Введите новое описание:"),
        TextInput("edit_desc", on_success=on_edit_description),
        state=ManageEventSG.edit_description,
    ),
)


