import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Radio, ScrollingGroup

from states import ManageOrgStructureSG
from dialogs.org_structure.edit.handlers import *
from dialogs.org_structure.edit.getters import *

logger = logging.getLogger(__name__)


list_window = Window(
    Const("📋 Список мероприятий:"),
    ScrollingGroup(
        Radio(
            checked_text=Format("✏️ {item[0]}"),
            unchecked_text=Format("✏️ {item[0]}"),
            id="org_structure_radio",
            item_id_getter=lambda x: x[1],
            items="org_structures",
            on_click=on_org_structure_selected,
        ),
        id="org_structure_scroll",
        width=1,
        height=5,
    ),
    Cancel(
        Const("❌ Выйти из режима редактирования"), id="exit_editing", on_click=on_exit
    ),
    state=ManageOrgStructureSG.list,
    getter=get_org_structure_list,
)

org_structure_detail_window = Window(
    Const("Выберите действие с мероприятием:"),
    Format("<b>{org_structure_title}</b>"),
    Format("{org_structure_description}"),
    Row(
        Button(Const("✏️ Название"), id="edit_title", on_click=on_edit_title_start),
        Button(Const("✏️ Описание"), id="edit_desc", on_click=on_edit_description_start),
    ),
    Row(
        Button(
            Const("✏️ Файл"),
            id="edit_file",
            on_click=lambda c, w, d, **k: d.switch_to(ManageOrgStructureSG.edit_file),
        ),
        Button(Const("🗑 Удалить"), id="delete", on_click=on_delete_org_structure),
    ),
    Button(
        Const("⬅️ Назад"),
        id="back",
        on_click=lambda c, w, d, **k: d.switch_to(ManageOrgStructureSG.list),
    ),
    state=ManageOrgStructureSG.org_structure_action,
    getter=get_org_structure_details,
)


edit_title_window = Window(
    Const("Редактирование названия мероприятия:"),
    Format("Вы хотите изменить название: \n<b>{org_structure_title}</b>"),
    TextInput("edit_title", on_success=on_edit_title),
    Cancel(Const("❌ Отмена")),
    state=ManageOrgStructureSG.edit_title,
    getter=get_org_structure_details,
)


edit_description_window = Window(
    Const("Редактирование описания мероприятия:"),
    Format("<b>{org_structure_title}</b>"),
    Format("Вы хотите изменить описание: \n{org_structure_description}"),
    TextInput("edit_desc", on_success=on_edit_description),
    Cancel(Const("❌ Отмена")),
    state=ManageOrgStructureSG.edit_description,
    getter=get_org_structure_details,
)


edit_file_window = Window(
    Const("📎 Отправьте новый файл (только документ):"),
    MessageInput(on_edit_file),
    Cancel(Const("❌ Отмена")),
    state=ManageOrgStructureSG.edit_file,
    getter=get_org_structure_details,
)

dialog = Dialog(
    list_window,
    org_structure_detail_window,
    edit_title_window,
    edit_description_window,
    edit_file_window,
)
