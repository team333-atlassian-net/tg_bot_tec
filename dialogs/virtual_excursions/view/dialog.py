from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import (
    Back,
    Next,
    Cancel,
    Row,
    Select,
    ScrollingGroup,
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.media import DynamicMedia
from states import ExcursionViewSG
from dao.virtual_excursions import *
from dialogs.virtual_excursions.view.getters import *
from dialogs.virtual_excursions.view.handlers import *

virtex_list_window = Window(
    Const("Выберите виртуальную экскурсию:"),
    ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id="virtex_select",
            item_id_getter=lambda item: item[0],
            items="virtexs",
            on_click=on_virtex_selected,
        ),
        id="virtexs",
        width=1,
        height=5,
    ),
    Cancel(Const("❌ Отмена")),
    state=ExcursionViewSG.list,
    getter=get_virtex_list,
)

virtex_detail_window = Window(
    Format("📌 <b>{virtex.title}</b>" "\n\n{virtex.description}"),
    Select(
        Format("{item[1].name}"),
        id="virtex_material_select",
        item_id_getter=lambda item: item[0],
        items="materials",
        on_click=on_material_selected,
    ),
    Row(Back(Const("⬅️ Назад")), Cancel(Const("❌ Закрыть"))),
    state=ExcursionViewSG.detail,
    getter=get_virtex_detail,
)

material_window = Window(
    DynamicMedia("file", when="file"),
    Format("{text}", when="text"),
    Row(Back(Const("⬅️ Вернуться к материалам экскурсии")), Cancel(Const("❌ Закрыть"))),
    state=ExcursionViewSG.material,
    getter=material_getter,
)

dialog = Dialog(virtex_list_window, virtex_detail_window, material_window)
