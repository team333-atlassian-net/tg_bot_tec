from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, ScrollingGroup, Radio

from states import CompanyInfoViewSG
from dialogs.company_info.view.handlers import *
from dialogs.company_info.view.getters import *


structure_list_window = Window(
    Const("🏢 Выберите раздел:"),
    ScrollingGroup(
        Radio(
            checked_text=Format("{item[1]}"),
            unchecked_text=Format("{item[1]}"),
            id="company_info_radio",
            item_id_getter=lambda x: x[0],
            items="company_info",
            on_click=on_company_info_selected,
        ),
        id="structure_scroll",
        width=1,
        height=5,
    ),
    Cancel(Const("❌ Отмена")),
    state=CompanyInfoViewSG.list,
    getter=get_company_info_list,
)

structure_detail_window = Window(
    Format("📌 <b>{company_info.title}</b>\n\n{content}"),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Закрыть")),
    ),
    state=CompanyInfoViewSG.detail,
    getter=get_company_info_detail,
)

dialog = Dialog(
    structure_list_window,
    structure_detail_window,
)
