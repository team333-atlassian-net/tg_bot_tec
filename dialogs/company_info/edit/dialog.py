import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Radio, ScrollingGroup

from states import ManageCompanyInfoSG
from dialogs.company_info.edit.handlers import *
from dialogs.company_info.edit.getters import *

logger = logging.getLogger(__name__)


list_window = Window(
    Const("📋 Список мероприятий:"),
    ScrollingGroup(
        Radio(
            checked_text=Format("✏️ {item[0]}"),
            unchecked_text=Format("✏️ {item[0]}"),
            id="company_info_radio",
            item_id_getter=lambda x: x[1],
            items="company_info",
            on_click=on_company_info_selected,
        ),
        id="company_info_scroll",
        width=1,
        height=5,
    ),
    Cancel(
        Const("❌ Выйти из режима редактирования"), id="exit_editing", on_click=on_exit
    ),
    state=ManageCompanyInfoSG.list,
    getter=get_company_info_list,
)

company_info_detail_window = Window(
    Const("Выберите действие с мероприятием:"),
    Format("<b>{company_info_title}</b>"),
    Format("{company_info_description}"),
    Row(
        Button(Const("✏️ Название"), id="edit_title", on_click=on_edit_title_start),
        Button(Const("✏️ Описание"), id="edit_desc", on_click=on_edit_description_start),
    ),
    Row(
        Button(
            Const("✏️ Файл"),
            id="edit_file",
            on_click=lambda c, w, d, **k: d.switch_to(ManageCompanyInfoSG.edit_file),
        ),
        Button(
            Const("✏️ Фото"),
            id="edit_image",
            on_click=lambda c, w, d, **k: d.switch_to(ManageCompanyInfoSG.edit_image),
        ),
    ),
    Button(Const("🗑 Удалить"), id="delete", on_click=on_delete_company_info),
    Button(
        Const("⬅️ Назад"),
        id="back",
        on_click=lambda c, w, d, **k: d.switch_to(ManageCompanyInfoSG.list),
    ),
    Cancel(Const("❌ Выйти"), id="exit_editing", on_click=on_exit),
    state=ManageCompanyInfoSG.company_info_action,
    getter=get_company_info_details,
)


edit_title_window = Window(
    Const("Редактирование названия мероприятия:"),
    Format("Вы хотите изменить название: \n<b>{company_info_title}</b>"),
    TextInput("edit_title", on_success=on_edit_title),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(
                ManageCompanyInfoSG.company_info_action
            ),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageCompanyInfoSG.edit_title,
    getter=get_company_info_details,
)


edit_description_window = Window(
    Const("Редактирование описания мероприятия:"),
    Format("<b>{company_info_title}</b>"),
    Format("Вы хотите изменить описание: \n{company_info_description}"),
    TextInput("edit_desc", on_success=on_edit_description),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(
                ManageCompanyInfoSG.company_info_action
            ),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageCompanyInfoSG.edit_description,
    getter=get_company_info_details,
)


edit_file_window = Window(
    Const("📎 Отправьте новый файл (только документ):"),
    MessageInput(on_file_edit),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(
                ManageCompanyInfoSG.company_info_action
            ),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageCompanyInfoSG.edit_file,
    getter=get_company_info_details,
)

edit_image_window = Window(
    Const("📎 Отправьте новое изображение:"),
    MessageInput(on_image_edit),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back",
            on_click=lambda c, w, d, **k: d.switch_to(
                ManageCompanyInfoSG.company_info_action
            ),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageCompanyInfoSG.edit_image,
    getter=get_company_info_details,
)

dialog = Dialog(
    list_window,
    company_info_detail_window,
    edit_title_window,
    edit_description_window,
    edit_file_window,
    edit_image_window,
)
