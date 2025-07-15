import logging
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import (
    Button, Cancel, Row, Radio, ScrollingGroup
)
from dao.org_structure import delete_org_structure, get_all_org_structures, get_org_structure_by_id, update_org_structure


logger = logging.getLogger(__name__)

class ManageOrgStructureSG(StatesGroup):
    list = State()
    org_structure_action = State()
    edit_title = State()
    edit_description = State()
    edit_file = State()


# --- Геттеры ---

async def get_org_structure_list(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает список всех мероприятий.
    """
    org_structures = await get_all_org_structures()
    return {"org_structures": [(o.title, str(o.id)) for o in org_structures]}


async def get_org_structure_details(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает детали выбранного раздела.
    """
    org_structure_id = dialog_manager.dialog_data.get("org_structure_id")
    if not org_structure_id:
        return {"org_structure_title": "Неизвестный раздел оргструктуры", "org_structure_description": ""}
    org_structure = await get_org_structure_by_id(int(org_structure_id))
    if not org_structure:
        return {"org_structure_title": "Информация не найдена", "org_structure_description": ""}
    return {
        "org_structure_title": org_structure.title,
        "org_structure_description": org_structure.content,
    }


# --- Коллбэки ---

async def on_org_structure_selected(callback: CallbackQuery, widget, manager: DialogManager, item_id: str):
    """
    Сохраняет выбранный раздел и переключается на детали.
    """
    manager.dialog_data["org_structure_id"] = item_id
    await manager.switch_to(ManageOrgStructureSG.org_structure_action)


async def on_edit_title_start(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Переход к окну редактирования названия.
    """
    await dialog_manager.switch_to(ManageOrgStructureSG.edit_title)


async def on_edit_description_start(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Переход к окну редактирования описания.
    """
    await dialog_manager.switch_to(ManageOrgStructureSG.edit_description)


async def on_edit_title(message: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Сохраняет новое название и завершает диалог.
    """
    org_structure_id = dialog_manager.dialog_data.get("org_structure_id")
    if org_structure_id:
        await update_org_structure(int(org_structure_id), value.get_value(), None)
        await message.answer("✏️ Название обновлено.")
        logger.info("Админ обновил название (/manage_org_structures)")
    await dialog_manager.done()


async def on_edit_description(message: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Сохраняет новое описание и завершает диалог.
    """
    org_structure_id = dialog_manager.dialog_data.get("org_structure_id")
    if org_structure_id:
        await update_org_structure(int(org_structure_id), None, value.get_value())
        await message.answer("📝 Описание обновлено.")
        logger.info("Админ обновил описание (/manage_org_structures)")
    await dialog_manager.done()

async def on_edit_file(message: Message, widget, dialog_manager: DialogManager):
    """
    Сохраняет новый файл и завершает диалог.
    """
    org_structure_id = dialog_manager.dialog_data.get("org_structure_id")
    file_id = None
    if message.document:
        file_id = message.document.file_id

    if file_id and org_structure_id:
        await update_org_structure(int(org_structure_id), None, None, file_id=file_id)
        await message.answer("📎 Файл обновлён.")
        logger.info("Админ обновил файл (/manage_org_structures)")
        await dialog_manager.done()
    else:
        await message.answer("❌ Пожалуйста, отправьте документ.")

async def on_delete_org_structure(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Удаляет выбранное мероприятие.
    """
    org_structure_id = dialog_manager.dialog_data.get("org_structure_id")
    if org_structure_id:
        await delete_org_structure(int(org_structure_id))
        await callback.message.answer("✅ Мероприятие удалено.")
        logger.info("Администратор удалил мероприятие (/manage_org_structures)")
    await dialog_manager.done()


async def on_exit(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Выход из режима редактирования.
    """
    await callback.message.answer("❌ Вы вышли из режима редактирования.")
    await dialog_manager.done()


# --- Окна ---

list_window = Window(
    Const("📋 Список мероприятий:"),
    ScrollingGroup(
        Radio(
            checked_text=Format("✏️ {item[0]}"),
            unchecked_text=Format("✏️ {item[0]}"),
            id="org_structure_radio",
            item_id_getter=lambda x: x[1],
            items="org_structures",
            on_click=on_org_structure_selected,
        ),
        id="org_structure_scroll",
        width=1,
        height=5,
    ),
    Cancel(Const("❌ Выйти из режима редактирования"), id="exit_editing", on_click=on_exit),
    state=ManageOrgStructureSG.list,
    getter=get_org_structure_list,
)

org_structure_detail_window = Window(
    Const("Выберите действие с мероприятием:"),
    Format("<b>{org_structure_title}</b>"),
    Format("{org_structure_description}"),
    Row(
        Button(Const("✏️ Название"), id="edit_title", on_click=on_edit_title_start),
        Button(Const("✏️ Описание"), id="edit_desc", on_click=on_edit_description_start),
    ),
    Row(
        Button(Const("✏️ Файл"), id="edit_file", on_click=lambda c, w, d, **k: d.switch_to(ManageOrgStructureSG.edit_file)),
        Button(Const("🗑 Удалить"), id="delete", on_click=on_delete_org_structure),
    ),
    Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageOrgStructureSG.list)),
    state=ManageOrgStructureSG.org_structure_action,
    getter=get_org_structure_details,
)


edit_title_window = Window(
    Const("Редактирование названия мероприятия:"),
    Format("Вы хотите изменить название: \n<b>{org_structure_title}</b>"),
    TextInput("edit_title", on_success=on_edit_title),
    Cancel(Const("❌ Отмена")),
    state=ManageOrgStructureSG.edit_title,
    getter=get_org_structure_details,
)


edit_description_window = Window(
    Const("Редактирование описания мероприятия:"),
    Format("<b>{org_structure_title}</b>"),
    Format("Вы хотите изменить описание: \n{org_structure_description}"),
    TextInput("edit_desc", on_success=on_edit_description),
    Cancel(Const("❌ Отмена")),
    state=ManageOrgStructureSG.edit_description,
    getter=get_org_structure_details,
)


edit_file_window = Window(
    Const("📎 Отправьте новый файл (только документ):"),
    MessageInput(on_edit_file),
    Cancel(Const("❌ Отмена")),
    state=ManageOrgStructureSG.edit_file,
    getter=get_org_structure_details,
)

manage_org_structure_dialog = Dialog(
    list_window,
    org_structure_detail_window,
    edit_title_window,
    edit_description_window,
    edit_file_window
)
