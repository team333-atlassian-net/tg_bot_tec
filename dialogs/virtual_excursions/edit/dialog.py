import logging
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.kbd import (
    Back,
    Next,
    Cancel,
    Row,
    Button,
    SwitchTo,
    Group,
    Select,
    ScrollingGroup,
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram.enums import ContentType
from aiogram.enums import ContentType
from states import ExcursionEditSG
from dao.virtual_excursions import *
from dialogs.virtual_excursions.edit.getters import *
from dialogs.virtual_excursions.edit.handlers import *

logger = logging.getLogger(__name__)

virtex_list_window = Window(
    Const("Выберите экскурсию для редактирования"),
    ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id="virtex_select",
            item_id_getter=lambda item: item[0],
            items="virtexs",
            on_click=on_virtex_selected,
        ),
        id="virtexs",
        width=3,
        height=1,
    ),
    Cancel(Const("❌ Отмена")),
    state=ExcursionEditSG.list,
    getter=get_excursion_list,
)

virtex_detail_window = Window(
    Format(
        "📌 Название экскурсии: {virtex.title}\n\n"
        "Описание экскурсии:{virtex.description}\n\n"
        "<b>Для редактирования материала нажмите соответсвтующую кнопку с названием материала</b>"
    ),
    Select(
        Format("{item[1].name}"),
        id="excursion_material_select",
        item_id_getter=lambda item: item[0],
        items="materials",
        on_click=on_material_selected,
    ),
    Row(Back(Const("⬅️ Назад")), Cancel(Const("❌ Закрыть"))),
    Group(
        Button(
            Const("Редактировать название экскурсии"),
            on_click=on_press_edit_virtex_title,
            id="edit_virtex_title_btn",
        ),
        Button(
            Const("Редактировать описание экскурсии"),
            on_click=on_press_edit_virtex_description,
            id="edit_virtex_description_btn",
        ),
        Button(
            Const("Добавить материал"),
            on_click=on_press_add_material,
            id="add_material_btn",
        ),
        Button(
            Const("Удалить экскурсию"),
            on_click=on_press_delete_virtex,
            id="delete_virtex_btn",
        ),
    ),
    state=ExcursionEditSG.detail,
    getter=get_excursion_detail,
)

virtex_material_window = Window(
    DynamicMedia("file", when="file"),
    Format("{text}", when="text"),
    Row(Back(Const("⬅️ Вернуться к материалам экскурсии")), Cancel(Const("❌ Закрыть"))),
    Group(
        Button(
            Const("Редактировать название материала"),
            id="edit_virtex_material_title_btn",
            on_click=on_press_edit_material_name,
        ),
        Button(
            Const("Удалить материал"),
            id="delete_virtex_material_btn",
            on_click=on_press_delete_material,
        ),
    ),
    state=ExcursionEditSG.material,
    getter=material_getter,
)

edit_virtex_title_window = Window(
    Const("Введите новое название экскурсии:"),
    MessageInput(on_edit_virtex_title),
    Cancel(Const("❌ Отмена")),
    state=ExcursionEditSG.edit_title,
)

edit_virtex_description_window = Window(
    Const("Введите новое описание экскурсии:"),
    MessageInput(on_edit_virtex_description),
    Cancel(Const("❌ Отмена")),
    state=ExcursionEditSG.edit_description,
)

delete_virtex_window = Window(
    Const("Введите новое название экскурсии:"),
    MessageInput(on_edit_virtex_title),
    Cancel(Const("❌ Отмена")),
    state=ExcursionEditSG.edit_title,
)


edit_material_name_window = Window(
    Const("Введите новое название материала:"),
    MessageInput(on_edit_material_name),
    Cancel(Const("❌ Отмена")),
    state=ExcursionEditSG.edit_material_name,
)


edit_material_window = Window(
    Const("Загрузите новый материал или введите в текстовом формате\n"),
    MessageInput(
        on_edit_material, content_types=[ContentType.DOCUMENT, ContentType.TEXT]
    ),
    Cancel(Const("❌ Отмена")),
    state=ExcursionEditSG.edit_material,
)


delete_virtex_window = Window(
    Const("Вы уверены, что хотите удалить экскурсию?"),
    Cancel(Const("❌ Отмена")),
    Button(
        Const("Да, удалить"), on_click=on_delete_virtex, id="confirm_delete_virtex_btn"
    ),
    state=ExcursionEditSG.delete_virtex,
)


delete_material_window = Window(
    Const("Вы уверены, что хотите удалить материал?"),
    Cancel(Const("❌ Отмена")),
    Button(
        Const("Да, удалить"),
        on_click=on_delete_material,
        id="confirm_delete_material_btn",
    ),
    state=ExcursionEditSG.delete_material,
)

dialog = Dialog(
    virtex_list_window,
    virtex_detail_window,
    virtex_material_window,
    edit_virtex_title_window,
    edit_virtex_description_window,
    delete_virtex_window,
    edit_material_name_window,
    edit_material_window,
    delete_material_window,
)
