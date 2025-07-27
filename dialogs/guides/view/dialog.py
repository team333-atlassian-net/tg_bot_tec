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
from states import GuideViewSG
from dao.virtual_excursions import *
from dialogs.guides.view.getters import *
from dialogs.guides.view.handlers import *

documents_list_window = Window(
    Const("Выберите документ, для которого нужны инструкции:"),
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
    state=GuideViewSG.documents,
    getter=documents_getter,
)

guides_list_window = Window(
    Format("📌 Инструкции для документа <b>{doc}</b>"),
    Select(
        Format("{item[1]}"),
        id="guides_select",
        item_id_getter=lambda item: item[0],
        items="guides",
        on_click=on_guide_select,
    ),
    Row(Back(Const("⬅️ Назад")), Cancel(Const("❌ Закрыть"))),
    state=GuideViewSG.guides,
    getter=guides_getter,
)

guide_content_window = Window(
    DynamicMedia("file", when="file"),
    Format("{text}", when="text"),
    Row(Back(Const("⬅️ Вернуться к другим инструкциям")), Cancel(Const("❌ Закрыть"))),
    state=GuideViewSG.guide,
    getter=guide_getter,
)

dialog = Dialog(documents_list_window, guides_list_window, guide_content_window)
