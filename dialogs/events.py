import logging
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Radio, ScrollingGroup, Button, Row
from aiogram_dialog.widgets.input import TextInput
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram_dialog.widgets.kbd import Back, Next, Cancel, Row, Button, Select

from dao.events import delete_event, get_all_events, update_event, get_event_by_id 

logger = logging.getLogger(__name__)


class EventsViewSG(StatesGroup):
    list = State()
    detail = State()

async def get_excursion_list(dialog_manager: DialogManager, **kwargs):
    events = await get_all_events()
    return {"events": [(str(e.id), e.title) for e in events]}


async def get_event_detail(dialog_manager: DialogManager, **kwargs):
    event_id = int(dialog_manager.dialog_data["selected_event_id"])
    event = await get_event_by_id(event_id)

    return {
        "event": event,
    }

async def on_event_selected(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["selected_event_id"] = int(selected_id)
    await manager.switch_to(EventsViewSG.detail)

async def detail_window_getter(dialog_manager: DialogManager, **kwargs):
    data = await get_event_detail(dialog_manager)
    return data

event_list_window = Window(
    Const("Выберите виртуальную экскурсию:"),
    Select(
        Format("{item[1]}"),
        id="excursion_select",
        item_id_getter=lambda x: x[0],
        items="events",
        on_click=on_event_selected,
    ),
    Cancel(Const("❌ Отмена")),
    state=EventsViewSG.list,
    getter=get_excursion_list,
)

event_detail_window = Window(
    Format("📌 <b>{event.title}</b>\n\n{event.description}"),
    Row(Back(Const("⬅️ Назад")), Cancel(Const("❌ Закрыть"))),
    state=EventsViewSG.detail,
    getter=detail_window_getter,
)

virtual_event_dialog = Dialog(event_list_window, event_detail_window)
