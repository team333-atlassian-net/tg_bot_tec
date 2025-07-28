import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Cancel, Row
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Calendar, Radio, ScrollingGroup

from states import ManageCanteenSG
from dialogs.canteen.edit.handlers import *
from dialogs.canteen.edit.getters import *


logger = logging.getLogger(__name__)


edit_choice_window = Window(
    Const("Что хотите отредактировать?"),
    Row(
        Button(
            Const("✏️ Информация о столовой"),
            id="edit_info",
            on_click=lambda c, b, m: m.switch_to(ManageCanteenSG.canteen_info_action),
        ),
        Button(
            Const("✏️ Меню"),
            id="edit_menu",
            on_click=lambda c, b, m: m.switch_to(ManageCanteenSG.select_menu),
        ),
    ),
    Cancel(Const("❌ Отмена")),
    state=ManageCanteenSG.choice,
)

canteen_info_detail_window = Window(
    Const("Выберите действие с информацией:"),
    Format("<b>Время начала работы: </b>{start_time}"),
    Format("<b>Время завершения работы: </b>{end_time}"),
    Format("{description}"),
    Row(
        Button(
            Const("✏️ Время начала работы"),
            id="edit_start_time",
            on_click=on_edit_start_time_start,
        ),
        Button(
            Const("✏️ Время завершения работы"),
            id="edit_end_time",
            on_click=on_edit_end_time_start,
        ),
    ),
    Row(
        Button(
            Const("✏️ Описание"),
            id="edit_file",
            on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.edit_description),
        ),
        Button(Const("🗑 Удалить"), id="delete", on_click=on_delete_canteen_info),
    ),
    Button(
        Const("⬅️ Назад"),
        id="back",
        on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.choice),
    ),
    state=ManageCanteenSG.canteen_info_action,
    getter=get_canteen_info,
)

edit_start_time_window = Window(
    Const("Редактирование время начала работы столовой:"),
    Format("Вы хотите изменить время: \n<b>{start_time}</b>"),
    TextInput("edit_start_time", on_success=on_edit_start_time),
    Row(
        Cancel(Const("❌ Отмена")),
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(
                ManageCanteenSG.canteen_info_action
            ),
        ),
    ),
    state=ManageCanteenSG.edit_start_time,
    getter=get_canteen_info,
)

edit_end_time_window = Window(
    Const("Редактирование время завершения работы столовой:"),
    Format("Вы хотите изменить время: \n<b>{end_time}</b>"),
    TextInput("edit_end_time", on_success=on_edit_end_time),
    Row(
        Cancel(Const("❌ Отмена")),
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(
                ManageCanteenSG.canteen_info_action
            ),
        ),
    ),
    state=ManageCanteenSG.edit_end_time,
    getter=get_canteen_info,
)

edit_description_window = Window(
    Const("Редактирование описание столовой:"),
    Format("<b>Время начала работы: </b>{start_time}"),
    Format("<b>Время завершения работы: </b>{end_time}"),
    Format("Вы хотите отредактировать описание: \n{description}"),
    TextInput("edit_description", on_success=on_edit_description),
    Row(
        Cancel(Const("❌ Отмена")),
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(
                ManageCanteenSG.canteen_info_action
            ),
        ),
    ),
    state=ManageCanteenSG.edit_description,
    getter=get_canteen_info,
)
select_menu_window = Window(
    Const("📅 Выберите дату меню для редактирования:"),
    ScrollingGroup(
        Radio(
            checked_text=Format(" {item[1]}"),
            unchecked_text=Format("{item[1]}"),
            id="menu_radio_admin",
            item_id_getter=lambda x: x[0],
            items="canteen_menus",
            on_click=on_select_menu,
        ),
        id="menu_scroll_admin",
        width=1,
        height=5,
    ),
    Row(
        Button(
            Const("📆 Календарь"),
            id="calendar_select",
            on_click=lambda c, w, d, **k: d.switch_to(
                ManageCanteenSG.confirm_menu_edit
            ),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageCanteenSG.select_menu,
    getter=get_menu_dates,
)

calendar_select_window = Window(
    Const("📆 Выберите дату:"),
    Calendar(id="admin_calendar", on_click=on_select_menu_by_date),
    Row(
        Cancel(Const("❌ Отмена")),
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.select_menu),
        ),
    ),
    state=ManageCanteenSG.confirm_menu_edit,
)

menu_edit_action_window = Window(
    Format("📌 <b>Меню на {formatted_date}</b>\n\n{content}"),
    Row(
        Button(
            Const("✏️ Редактировать текст"),
            id="edit_text",
            on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.edit_menu_text),
        ),
        Button(
            Const("📎 Заменить файл"),
            id="edit_file",
            on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.edit_menu_file),
        ),
    ),
    Row(
        Button(Const("🗑 Удалить файл"), id="delete_file", on_click=on_delete_menu_file),
        Button(Const("🗑 Удалить меню"), id="delete_menu", on_click=on_delete_menu),
    ),
    Row(
        Cancel(Const("❌ Отмена")),
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.select_menu),
        ),
    ),
    state=ManageCanteenSG.menu_edit_action,
    getter=get_selected_menu,
)

edit_menu_text_window = Window(
    Format("Редактирование меню на {formatted_date}:"),
    Format("Вы хотите изменить меню: \n<b>{content}</b>"),
    TextInput(id="menu_text_input", on_success=on_edit_menu_text),
    Row(
        Cancel(Const("❌ Отмена")),
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.menu_edit_action),
        ),
    ),
    state=ManageCanteenSG.edit_menu_text,
    getter=get_selected_menu,
)

edit_menu_file_window = Window(
    Format("Редактирование меню на {formatted_date}:"),
    Const("📎 Пришлите новый файл меню (фото или документ):"),
    MessageInput(on_edit_menu_file),
    Row(
        Cancel(Const("❌ Отмена")),
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.menu_edit_action),
        ),
    ),
    state=ManageCanteenSG.edit_menu_file,
    getter=get_selected_menu,
)


dialog = Dialog(
    edit_choice_window,
    canteen_info_detail_window,
    edit_start_time_window,
    edit_end_time_window,
    edit_description_window,
    select_menu_window,
    calendar_select_window,
    menu_edit_action_window,
    edit_menu_text_window,
    edit_menu_file_window,
)
