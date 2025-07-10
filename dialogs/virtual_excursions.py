import logging
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.api.protocols import DialogManager
from aiogram.types import Message
from aiogram_dialog.widgets.input import MessageInput
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Document
from aiogram_dialog.widgets.kbd import Back, Next, Cancel, Row, Button, Select
from aiogram_dialog.widgets.text import Const, Format
from aiogram.enums import ContentType, ParseMode
from dao.virtual_excursions import (
    get_all_excursions,
    get_excursion_by_id,
    add_material,
    create_excursion,
)

logger = logging.getLogger(__name__)
# TODO вынести в отдельные файлы getters handlers


class ExcursionCreationSG(StatesGroup):
    title = State()
    description = State()
    confirm = State()
    upload_materials = State()


class ExcursionView(StatesGroup):
    list = State()
    detail = State()


async def get_excursion_list(dialog_manager: DialogManager, **kwargs):
    excursions = await get_all_excursions()
    return {"excursions": [(str(e.id), e.title) for e in excursions]}


async def get_excursion_detail(dialog_manager: DialogManager, **kwargs):
    excursion_id = int(dialog_manager.dialog_data["selected_excursion_id"])
    excursion = await get_excursion_by_id(excursion_id)
    materials = excursion.materials

    return {
        "excursion": excursion,
        "materials": materials,
    }


async def on_title_input(
    message: Message,
    widget: TextInput,
    dialog: DialogManager,
):
    """
    Обработчик успешного ввода заголовка.

    Сохраняет заголовок в dialog_data и переключается на состояние ввода описания.
    """
    dialog.dialog_data["title"] = message.text
    await dialog.switch_to(ExcursionCreationSG.description)


async def on_description_input(
    message: Message, widget: TextInput, dialog: DialogManager
):
    """
    Обработчик ввода описания.

    """
    dialog.dialog_data["description"] = message.text
    await dialog.switch_to(ExcursionCreationSG.confirm)


async def on_description_skip(callback, button: Button, dialog: DialogManager):
    dialog.dialog_data["description"] = "—"
    await dialog.switch_to(ExcursionCreationSG.confirm)


async def on_document_upload(
    message: Message, widget: MessageInput, dialog: DialogManager
):
    if not (message.document and message.text):
        return

    doc = message.document
    text = message.text
    excursion_id = dialog.dialog_data.get("excursion_id")
    file_id = doc.file_id if doc else None
    file_name = doc.file_name if doc else None
    add_material(excursion_id, file_id, file_name, text)

    await message.answer(f"✅ Материал «{doc.file_name}» добавлен.")


async def on_confirm_press(callback, button, manager: DialogManager):
    title = manager.dialog_data.get("title")
    description = manager.dialog_data.get("description")

    excursion = await create_excursion(title, description)

    manager.dialog_data["excursion_id"] = excursion.id
    await manager.switch_to(ExcursionCreationSG.upload_materials)


async def on_excursion_selected(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["selected_excursion_id"] = int(selected_id)
    await manager.switch_to(ExcursionView.detail)


async def send_file_callback(c, button, manager: DialogManager):
    telegram_file_id = button.widget_id.split("_", 1)[-1]
    await c.message.answer_document(telegram_file_id)


def material_button(material):
    return Button(
        Const(material.file_name or "📄 Материал"),
        id=f"file_{material.telegram_file_id}",
        on_click=send_file_callback,
    )


async def detail_window_getter(dialog_manager: DialogManager, **kwargs):
    data = await get_excursion_detail(dialog_manager)
    data["material_buttons"] = [material_button(m) for m in data["materials"]]
    return data


# async def get_material_buttons(dialog_manager: DialogManager, **kwargs):
#     materials = await get_excursion_detail(dialog_manager)
#     return [Button(text=m.title) for m in materials]

# --- Окна ---

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

upload_materials_window = Window(
    Const(
        "Загрузите материалы (PDF, презентации и т.д.):\n\nМожно отправить несколько файлов."
    ),
    MessageInput(
        on_document_upload, content_types=[ContentType.DOCUMENT, ContentType.TEXT]
    ),
    Row(
        Button(
            Const("✅ Завершить"), id="finish_upload", on_click=lambda c, b, m: m.done()
        ),
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=ExcursionCreationSG.upload_materials,
)

excursion_list_window = Window(
    Const("Выберите виртуальную экскурсию:"),
    Select(
        Format("{item[1]}"),
        id="excursion_select",
        item_id_getter=lambda x: x[0],
        items="excursions",
        on_click=on_excursion_selected,
    ),
    Cancel(Const("❌ Отмена")),
    state=ExcursionView.list,
    getter=get_excursion_list,
)

excursion_detail_window = Window(
    Format("📌 <b>{excursion.title}</b>\n\n{excursion.description}"),
    Row(Back(Const("⬅️ Назад")), Cancel(Const("❌ Закрыть"))),
    state=ExcursionView.detail,
    getter=detail_window_getter,
)

create_virtual_excursion_dialog = Dialog(
    title_window, description_window, confirm_window, upload_materials_window
)

virtual_excursion_dialog = Dialog(excursion_list_window, excursion_detail_window)
