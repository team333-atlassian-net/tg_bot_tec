from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, ScrollingGroup, Radio

from dialogs.org_structure.view.handlers import *
from dialogs.org_structure.view.getters import *
from states import OrgStructureViewSG

structure_list_window = Window(
    Const("🏢 Выберите раздел организационной структуры:"),
    ScrollingGroup(
        Radio(
            checked_text=Format("{item[1]}"),
            unchecked_text=Format("{item[1]}"),
            id="structure_radio",
            item_id_getter=lambda x: x[0],
            items="structures",
            on_click=on_structure_selected,
        ),
        id="structure_scroll",
        width=1,
        height=5,
    ),
    Cancel(Const("❌ Отмена")),
    state=OrgStructureViewSG.list,
    getter=get_structure_list,
)

structure_detail_window = Window(
    Format("📌 <b>{structure.title}</b>\n\n{content}"),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Закрыть")),
    ),
    state=OrgStructureViewSG.detail,
    getter=get_structure_detail,
)

dialog = Dialog(
    structure_list_window,
    structure_detail_window,
)
