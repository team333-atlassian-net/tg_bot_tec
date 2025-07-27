import logging
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput
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
from states import GuideCreationSG
from dialogs.guides.create.handlers import *
from dialogs.guides.create.getters import *
from dialogs.guides.view.getters import *

logger = logging.getLogger(__name__)

select_doc_window = Window(
    Const(
        "Выберите документ, для которого хотите добавить инструкцию, "
        "или введите название для создания нового:"
    ),
    ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id="doc_select",
            item_id_getter=lambda item: item[0],
            items="docs",
            on_click=on_doc_selected,
        ),
        id="docs",
        width=1,
        height=3,
    ),
    MessageInput(on_doc_name_input),
    Cancel(Const("❌ Отмена")),
    state=GuideCreationSG.document,
    getter=documents_getter,
)

title_window = Window(
    Const("Введите название инструкции:"),
    MessageInput(on_title_input),
    Row(Cancel(Const("❌ Отмена")), Back(Const("⬅️ Назад"))),
    state=GuideCreationSG.title,
)


upload_guide_content_window = Window(
    Const("Загрузите файл инструкции или введите её в текстовом формате:\n"),
    MessageInput(
        on_guide_content_upload, content_types=[ContentType.DOCUMENT, ContentType.TEXT]
    ),
    Group(
        Button(
            Const("✅ Завершить"), id="finish_upload", on_click=lambda c, b, m: m.done()
        ),
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
        width=3,
    ),
    state=GuideCreationSG.upload_content,
)


guide_end_window = Window(
    Format(
        "✅ Инструкция «{dialog_data[title]}» для оформления документа «{dialog_data[doc]}» добавлена."
    ),
    Group(
        Cancel(Const("❌ Отмена")),
        Button(Const("✅ Завершить"), id="finish", on_click=lambda c, b, m: m.done()),
        SwitchTo(
            Const("Добавить еще инструкцию"),
            state=GuideCreationSG.title,
            id="add_another_material",
        ),
        width=2,
    ),
    state=GuideCreationSG.end,
)


dialog = Dialog(
    select_doc_window, title_window, upload_guide_content_window, guide_end_window
)
