import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Radio, ScrollingGroup

from states import ManageEventSG
from dialogs.events.edit.handlers import *
from dialogs.events.edit.getters import *

logger = logging.getLogger(__name__)


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
        height=5,
    ),
    Cancel(
        Const("❌ Выйти из режима редактирования"), id="exit_editing", on_click=on_exit
    ),
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
    ),
    Button(Const("🗑 Удалить"), id="delete", on_click=on_delete_event),
    Button(
        Const("⬅️ Назад"),
        id="back",
        on_click=lambda c, w, d, **k: d.switch_to(ManageEventSG.list),
    ),
    state=ManageEventSG.event_action,
    getter=get_event_details,
)

edit_title_window = Window(
    Const("Редактирование названия мероприятия:"),
    Format("Вы хотите изменить название: \n<b>{event_title}</b>"),
    TextInput("edit_title", on_success=on_edit_title),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(ManageEventSG.event_action),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageEventSG.edit_title,
    getter=get_event_details,
)


edit_description_window = Window(
    Const("Редактирование описания мероприятия:"),
    Format("<b>{event_title}</b>"),
    Format("Вы хотите изменить описание: \n{event_description}"),
    TextInput("edit_desc", on_success=on_edit_description),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(ManageEventSG.event_action),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageEventSG.edit_description,
    getter=get_event_details,
)


dialog = Dialog(
    list_window,
    event_detail_window,
    edit_title_window,
    edit_description_window,
)
