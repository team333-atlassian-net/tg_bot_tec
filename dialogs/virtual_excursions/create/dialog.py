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
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram.enums import ContentType
from aiogram.enums import ContentType
from states import ExcursionCreationSG
from dialogs.virtual_excursions.create.handlers import *

logger = logging.getLogger(__name__)

title_window = Window(
    Const("Введите название экскурсии:"),
    MessageInput(on_title_input),
    Cancel(Const("❌ Отмена")),
    state=ExcursionCreationSG.title,
)

description_window = Window(
    Const("Введите описание экскурсии (необязательно):"),
    MessageInput(on_description_input),
    Row(
        Button(
            Const("➡️ Пропустить"),
            id="skip_description",
            on_click=on_description_skip,
        ),
        Back(Const("⬅️ Назад")),
    ),
    state=ExcursionCreationSG.description,
)

confirm_window = Window(
    Format(
        "Подтвердите создание экскурсии:\n\nНазвание: {dialog_data[title]}\nОписание: {dialog_data[description]}"
    ),
    Row(
        Button(Const("✅ Сохранить"), id="confirm", on_click=on_confirm_press),
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=ExcursionCreationSG.confirm,
)


material_name_window = Window(
    Const("Введите название материала:"),
    MessageInput(on_material_name_input),
    Cancel(Const("❌ Отмена")),
    state=ExcursionCreationSG.material_name,
)


upload_materials_window = Window(
    Const(
        "Загрузите материал (PDF, презентации и т.д.) или введите в текстовом формате:\n"
    ),
    MessageInput(
        on_document_upload, content_types=[ContentType.DOCUMENT, ContentType.TEXT]
    ),
    Group(
        Button(
            Const("✅ Завершить"), id="finish_upload", on_click=lambda c, b, m: m.done()
        ),
        Cancel(Const("❌ Отмена")),
        width=2,
    ),
    state=ExcursionCreationSG.upload_materials,
)


material_end_window = Window(
    Format("✅ Материал «{dialog_data[material_name]}» добавлен."),
    Group(
        Cancel(Const("❌ Отмена")),
        SwitchTo(
            Const("Добавить еще материал"),
            state=ExcursionCreationSG.material_name,
            id="add_another_material",
        ),
        width=2,
    ),
    state=ExcursionCreationSG.material_end,
)


dialog = Dialog(
    title_window,
    description_window,
    confirm_window,
    upload_materials_window,
    material_name_window,
    material_end_window,
)
