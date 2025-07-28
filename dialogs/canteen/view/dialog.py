from datetime import date
import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import (
    Back,
    Cancel,
    Row,
    Button,
    ScrollingGroup,
    Radio,
    Calendar,
)

from states import CanteenViewSG
from dialogs.canteen.view.handlers import *
from dialogs.canteen.view.getters import *

logger = logging.getLogger(__name__)

start_window = Window(
    Const("🍽 Что вы хотите посмотреть?"),
    Row(
        Button(
            Const("🏢 Информация о столовой"),
            id="info",
            on_click=lambda c, b, m: m.switch_to(CanteenViewSG.info),
        ),
        Button(
            Const("📋 Меню"),
            id="menu",
            on_click=lambda c, b, m: m.switch_to(CanteenViewSG.menu_list),
        ),
    ),
    Cancel(Const("❌ Отмена")),
    state=CanteenViewSG.start,
)


menu_list_window = Window(
    Const("📅 Выберите дату меню:"),
    ScrollingGroup(
        Radio(
            checked_text=Format("{item[1]}"),
            unchecked_text=Format("{item[1]}"),
            id="menu_radio",
            item_id_getter=lambda x: x[0],
            items="canteen_menus",
            on_click=on_menu_selected,
        ),
        id="menu_scroll",
        width=1,
        height=5,
    ),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back_to_menu",
            on_click=lambda c, b, m: m.switch_to(CanteenViewSG.start),
        ),
        Button(
            Const("📆 Календарь"),
            id="calendar",
            on_click=lambda c, b, m: m.switch_to(CanteenViewSG.calendar),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=CanteenViewSG.menu_list,
    getter=get_canteen_menu_list,
)


menu_detail_window = Window(
    Format("📌 <b>Меню на {formatted_date}</b>\n\n{content}"),
    Row(Back(Const("⬅️ Назад")), Cancel(Const("❌ Закрыть"))),
    state=CanteenViewSG.menu_detail,
    getter=get_canteen_menu_detail,
)


calendar_window = Window(
    Const("📆 Выберите дату меню:"),
    Calendar(id="menu_calendar", on_click=on_date_selected),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back_to_menu",
            on_click=lambda c, b, m: m.switch_to(CanteenViewSG.menu_list),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=CanteenViewSG.calendar,
)

canteen_info_window = Window(
    Format("{content}"),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back_to_menu",
            on_click=lambda c, b, m: m.switch_to(CanteenViewSG.start),
        ),
        Cancel(Const("❌ Закрыть")),
    ),
    state=CanteenViewSG.info,
    getter=get_canteen_info_detail,
)

dialog = Dialog(
    start_window,
    menu_list_window,
    menu_detail_window,
    calendar_window,
    canteen_info_window,
)
