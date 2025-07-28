import logging

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Select, Radio, ScrollingGroup

from states import EventsViewSG
from dialogs.events.view.handlers import *
from dialogs.events.view.getters import *

logger = logging.getLogger(__name__)

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
    Row(Back(Const("⬅️ Назад")), Cancel(Const("❌ Закрыть"))),
    state=EventsViewSG.detail,
    getter=detail_window_getter,
)

dialog = Dialog(event_list_window, event_detail_window)
