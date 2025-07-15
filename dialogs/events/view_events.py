import logging

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Select, Radio, ScrollingGroup

from dao.events import get_all_events, get_event_by_id

logger = logging.getLogger(__name__)


class EventsViewSG(StatesGroup):
    """
    Состояния диалога просмотра мероприятий.
    """
    list = State()
    detail = State()


async def get_event_list(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для получения списка мероприятий.
    Возвращает список кортежей (id, title) мероприятий,
    который используется для отображения в Select или Radio.

    Returns:
        dict: {'events': [(id, title), ...]}
    """
    events = await get_all_events()
    return {"events": [(str(e.id), e.title) for e in events]}


async def get_event_detail(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для получения подробной информации о выбранном мероприятии.
    Использует сохранённый event_id из dialog_data.

    Returns:
        dict: {'event': Event}
    """
    event_id = int(dialog_manager.dialog_data["selected_event_id"])
    event = await get_event_by_id(event_id)
    return {"event": event}


async def on_event_selected(callback, widget: Select, manager: DialogManager, selected_id: str):
    """
    Обработчик выбора мероприятия из списка.
    Сохраняет выбранный event_id в dialog_data и переключает состояние на detail.

    Args:
        selected_id (str): ID выбранного мероприятия.
    """
    manager.dialog_data["selected_event_id"] = int(selected_id)
    await manager.switch_to(EventsViewSG.detail)


async def detail_window_getter(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для окна с подробной информацией о мероприятии.
    Используется для передачи данных в шаблон Format.

    Returns:
        dict: {'event': Event}
    """
    data = await get_event_detail(dialog_manager)
    return data


# Окно списка мероприятий
event_list_window = Window(
    Const("Выберите мероприятие:"),
    ScrollingGroup(
        Radio(
            Format("{item[1]}"),  # Выбранный вариант
            Format("{item[1]}"),  # Не выбранный
            id="event_radio",
            item_id_getter=lambda x: x[0],
            on_click=on_event_selected,
            items="events",
        ),
        id="event_scroll",
        width=1,
        height=5,
    ),
    Cancel(Const("❌ Отмена")),
    state=EventsViewSG.list,
    getter=get_event_list,
)

# Окно с деталями мероприятия
event_detail_window = Window(
    Format("📌 <b>{event.title}</b>\n\n{event.description}"),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Закрыть"))
    ),
    state=EventsViewSG.detail,
    getter=detail_window_getter,
)

# Диалог просмотра мероприятий
view_event_dialog = Dialog(event_list_window, event_detail_window)