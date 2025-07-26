import logging

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Button

from dao.org_structure import add_org_structure

logger = logging.getLogger(__name__)

class OrgStructureCreationSG(StatesGroup):
    """
    Состояния для диалога создания новой организационной структуры.
    """
    title = State()
    description = State()
    file = State()
    confirm = State()


async def on_title_input(message: Message, widget: TextInput, dialog: DialogManager):
    """
    Обрабатывает ввод названия организационной структуры.
    Сохраняет введённый текст в dialog_data и переходит к описанию.
    """
    dialog.dialog_data["title"] = message.text
    await dialog.switch_to(OrgStructureCreationSG.description)


async def on_description_input(message: Message, widget: TextInput, dialog: DialogManager):
    """
    Обрабатывает ввод описания организационной структуры.
    Сохраняет описание и переходит к загрузке файла.
    """
    dialog.dialog_data["description"] = message.text
    await dialog.switch_to(OrgStructureCreationSG.file)


async def on_file_input(message: Message, widget, dialog: DialogManager):
    """
    Обрабатывает загрузку документа.
    Сохраняет file_id и имя файла. Переходит к окну подтверждения.
    """
    file_id = None
    file_name = None
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name

    if file_id:
        dialog.dialog_data["file_id"] = file_id
        dialog.dialog_data["file_name"] = file_name
        await dialog.switch_to(OrgStructureCreationSG.confirm)
    else:
        await message.answer("❌ Пожалуйста, отправьте файл.")


async def on_description_skip(callback: CallbackQuery, button, dialog: DialogManager):
    """
    Обрабатывает нажатие кнопки "Пропустить" на этапе описания.
    Устанавливает значение описания в None и переходит к загрузке файла.
    """
    dialog.dialog_data["description"] = None
    await dialog.switch_to(OrgStructureCreationSG.file)


async def on_file_skip(callback: CallbackQuery, button, dialog: DialogManager):
    """
    Обрабатывает нажатие кнопки "Пропустить" на этапе загрузки файла.
    Устанавливает file_id в None и переходит к окну подтверждения.
    """
    dialog.dialog_data["file_id"] = None
    await dialog.switch_to(OrgStructureCreationSG.confirm)


async def get_confirm_data(dialog_manager: DialogManager, **kwargs):
    """
    Подготавливает данные для отображения в окне подтверждения.
    Возвращает название, описание (или '-') и имя файла (или '-').
    """
    title = dialog_manager.dialog_data.get("title")
    description = dialog_manager.dialog_data.get("description")
    file_name = dialog_manager.dialog_data.get("file_name")

    file_text = file_name if file_name else "-"
    description_text = description if description else "-"

    return {
        "dialog_data": {
            "title": title,
            "description": description_text,
            "file_text": file_text,
        }
    }


async def on_confirm_press(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Обрабатывает подтверждение создания новой оргструктуры.
    Сохраняет данные в БД и завершает диалог.
    """
    title = dialog_manager.dialog_data.get("title")
    description = dialog_manager.dialog_data.get("description")
    file_id = dialog_manager.dialog_data.get("file_id")

    if not title:
        await callback.message.answer("❌ Не удалось получить название.")
        return

    await add_org_structure(title, description, file_id)
    await callback.message.answer("✅ Информация об организационной структуре добавлена")
    logger.info("Администратор добавил новую информацию об оргструктуре (/add_event)")
    await dialog_manager.done()

# --- Окна ---

title_window = Window(
    Const("Введите название организационной структуры:"),
    MessageInput(on_title_input),
    Cancel(Const("❌ Отмена")),
    state=OrgStructureCreationSG.title,
)

description_window = Window(
    Const("Введите описание (необязательно):"),
    MessageInput(on_description_input),
    Row(
        Back(Const("⬅️ Назад")),
        Button(Const("➡️ Пропустить"), id="skip_desc", on_click=on_description_skip),
        Cancel(Const("❌ Отмена")),
    ),
    state=OrgStructureCreationSG.description,
)

file_window = Window(
    Const("Отправьте файл (необязательно):"),
    MessageInput(on_file_input),
    Row(
        Back(Const("⬅️ Назад")),
        Button(Const("➡️ Пропустить"), id="skip_file", on_click=on_file_skip),
        Cancel(Const("❌ Отмена")),
    ),
    state=OrgStructureCreationSG.file,
)


confirm_window = Window(
    Format(
        "Подтвердите создание информации об организационной структуре:\n\n"
        "Название: {dialog_data[title]}\n"
        "Описание: {dialog_data[description]}\n"
        "Файл: {dialog_data[file_text]}"
    ),
    Row(
        Button(Const("✅ Сохранить"), id="confirm", on_click=on_confirm_press),
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=OrgStructureCreationSG.confirm,
    getter=get_confirm_data,
)

create_org_structure_dialog = Dialog(
    title_window,
    description_window,
    file_window,
    confirm_window,
)
