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
from states import GuideEditSG
from dao.virtual_excursions import *
from dialogs.guides.view.getters import *
from dialogs.guides.edit.getters import *
from dialogs.guides.edit.handlers import *

logger = logging.getLogger(__name__)

docs_list_window = Window(
    Const("Выберите документ, инструкцию к которому хотите отредактировать"),
    ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id="doc_select",
            item_id_getter=lambda item: item[0],
            items="docs",
            on_click=on_doc_select,
        ),
        id="docs",
        width=1,
        height=3,
    ),
    Cancel(Const("❌ Отмена")),
    state=GuideEditSG.documents,
    getter=documents_getter,
)

guides_list_window = Window(
    Format("📌 Инструкции для документа <b>{doc}</b>"),
    ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id="guides_select",
            item_id_getter=lambda item: item[0],
            items="guides",
            on_click=on_guide_select,
        ),
    ),
    Row(Back(Const("⬅️ Назад")), Cancel(Const("❌ Закрыть"))),
    Group(
        Button(
            Const("Редактировать название документа"),
            on_click=on_press_edit_doc_name,
            id="edit_doc_name_btn",
        ),
        Button(
            Const("Добавить инструкцию"),
            on_click=on_press_add_guide,
            id="add_guide_btn",
        ),
        Button(
            Const("Удалить документ"),
            on_click=on_press_delete_doc,
            id="delete_doc_btn",
        ),
    ),
    state=GuideEditSG.guides,
    getter=guides_getter,
)

guide_content_window = Window(
    DynamicMedia("file", when="file"),
    Format("{text}", when="text"),
    Row(Back(Const("⬅️ Вернуться к другим инструкциям")), Cancel(Const("❌ Закрыть"))),
    Group(
        Button(
            Const("Редактировать название инструкции"),
            id="edit_guide_title_btn",
            on_click=on_press_edit_guide_title,
        ),
        Button(
            Const("Редактировать инструкцию"),
            id="edit_guide_content_btn",
            on_click=on_press_edit_guide_content,
        ),
        Button(
            Const("Удалить материал"),
            id="delete_guide_btn",
            on_click=on_press_delete_guide,
        ),
    ),
    state=GuideEditSG.guide,
    getter=guide_getter,
)

edit_doc_name_window = Window(
    Const("Введите новое название документа:"),
    MessageInput(on_edit_doc_name),
    Cancel(Const("❌ Отмена")),
    state=GuideEditSG.edit_doc_name,
)

edit_guide_title_window = Window(
    Const("Введите новое название инструкции:"),
    MessageInput(on_edit_guide_title),
    Cancel(Const("❌ Отмена")),
    state=GuideEditSG.edit_title,
)

edit_guide_content_window = Window(
    Const("Загрузите новый файл инструкции или введите в текстовом формате\n"),
    MessageInput(
        on_edit_guide_content, content_types=[ContentType.DOCUMENT, ContentType.TEXT]
    ),
    Cancel(Const("❌ Отмена")),
    state=GuideEditSG.edit_content,
)

delete_doc_window = Window(
    Const("Вы уверены, что хотите удалить документ?"),
    Cancel(Const("❌ Отмена")),
    Button(
        Const("Да, удалить"),
        on_click=on_delete_doc,
        id="confirm_delete_doc_btn",
    ),
    state=GuideEditSG.delete_doc,
)

delete_guide_window = Window(
    Const("Вы уверены, что хотите удалить инструкцию?"),
    Cancel(Const("❌ Отмена")),
    Button(
        Const("Да, удалить"),
        on_click=on_delete_guide,
        id="confirm_delete_guide_btn",
    ),
    state=GuideEditSG.delete_guide,
)

dialog = Dialog(
    docs_list_window,
    guides_list_window,
    guide_content_window,
    edit_doc_name_window,
    edit_guide_title_window,
    edit_guide_content_window,
    delete_doc_window,
    delete_guide_window,
)
