import logging
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import (
    Button, Cancel, Row, Radio, ScrollingGroup
)
from dao.company_info import delete_company_info, get_all_company_info, get_company_info_by_id, update_company_info

logger = logging.getLogger(__name__)

class ManageCompanyInfoSG(StatesGroup):
    list = State()
    company_info_action = State()
    edit_title = State()
    edit_description = State()
    edit_file = State()
    edit_image = State()


# --- Геттеры ---

async def get_company_info_list(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает список всех разделов с информацией.
    """
    company_info = await get_all_company_info()
    return {"company_info": [(c.title, str(c.id)) for c in company_info]}


async def get_company_info_details(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает детали выбранного раздела.
    """
    company_info_id = dialog_manager.dialog_data.get("company_info_id")
    if not company_info_id:
        return {"company_info_title": "Неизвестный раздел информации", "company_info_description": ""}
    company_info = await get_company_info_by_id(int(company_info_id))
    if not company_info:
        return {"company_info_title": "Информация не найдена", "company_info_description": ""}
    return {
        "company_info_title": company_info.title,
        "company_info_description": company_info.content,
    }


# --- Коллбэки ---

async def on_company_info_selected(callback: CallbackQuery, widget, manager: DialogManager, item_id: str):
    """
    Сохраняет выбранный раздел и переключается на детали.
    """
    manager.dialog_data["company_info_id"] = item_id
    await manager.switch_to(ManageCompanyInfoSG.company_info_action)


async def on_edit_title_start(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Переход к окну редактирования названия.
    """
    await dialog_manager.switch_to(ManageCompanyInfoSG.edit_title)


async def on_edit_description_start(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Переход к окну редактирования описания.
    """
    await dialog_manager.switch_to(ManageCompanyInfoSG.edit_description)


async def on_edit_title(message: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Сохраняет новое название и завершает диалог.
    """
    company_info_id = dialog_manager.dialog_data.get("company_info_id")
    if company_info_id:
        await update_company_info(int(company_info_id), value.get_value(), None)
        await message.answer("✏️ Название обновлено.")
        logger.info("Админ обновил название (/manage_company_info)")
    await dialog_manager.done()


async def on_edit_description(message: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Сохраняет новое описание и завершает диалог.
    """
    company_info_id = dialog_manager.dialog_data.get("company_info_id")
    if company_info_id:
        await update_company_info(int(company_info_id), None, value.get_value())
        await message.answer("📝 Описание обновлено.")
        logger.info("Админ обновил описание (/manage_company_info)")
    await dialog_manager.done()

async def on_file_edit(message: Message, widget, dialog_manager: DialogManager):
    """
    Сохраняет новый файл и завершает диалог.
    """
    company_info_id = dialog_manager.dialog_data.get("company_info_id")
    file_id = None
    if message.document:
        file_id = message.document.file_id

    if file_id and company_info_id:
        await update_company_info(int(company_info_id), None, None, file_id=file_id)
        await message.answer("📎 Файл обновлён.")
        logger.info("Админ обновил файл (/manage_company_info)")
        await dialog_manager.done()
    else:
        await message.answer("❌ Пожалуйста, отправьте документ.")

async def on_image_edit(message: Message, widget, dialog_manager: DialogManager):
    """
    Обрабатывает загрузку нового изображения или документа для CompanyInfo.
    Сохраняет file_id и завершает диалог.
    """
    company_info_id = dialog_manager.dialog_data.get("company_info_id")
    image_id = None

    if message.photo:
        image_id = message.photo[-1].file_id  # Самое большое по размеру фото

    if image_id and company_info_id:
        await update_company_info(int(company_info_id), None, None, None, image_id=image_id)
        await message.answer("📎 Изображение обновлено.")
        logger.info("Админ обновил фото (/manage_company_info)")
        await dialog_manager.done()
    else:
        await message.answer("❌ Пожалуйста, отправьте изображение.")


async def on_delete_company_info(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Удаляет выбранное мероприятие.
    """
    company_info_id = dialog_manager.dialog_data.get("company_info_id")
    if company_info_id:
        await delete_company_info(int(company_info_id))
        await callback.message.answer("✅ Информация удалена.")
        logger.info("Администратор удалил информацию о компании (/manage_company_info)")
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
            id="company_info_radio",
            item_id_getter=lambda x: x[1],
            items="company_info",
            on_click=on_company_info_selected,
        ),
        id="company_info_scroll",
        width=1,
        height=3,
    ),
    Cancel(Const("❌ Выйти из режима редактирования"), id="exit_editing", on_click=on_exit),
    state=ManageCompanyInfoSG.list,
    getter=get_company_info_list,
)

company_info_detail_window = Window(
    Const("Выберите действие с мероприятием:"),
    Format("<b>{company_info_title}</b>"),
    Format("{company_info_description}"),
    Row(
        Button(Const("✏️ Название"), id="edit_title", on_click=on_edit_title_start),
        Button(Const("✏️ Описание"), id="edit_desc", on_click=on_edit_description_start),
    ),
    Row(
        Button(Const("✏️ Файл"), id="edit_file", on_click=lambda c, w, d, **k: d.switch_to(ManageCompanyInfoSG.edit_file)),
        Button(Const("✏️ Фото"), id="edit_image", on_click=lambda c, w, d, **k: d.switch_to(ManageCompanyInfoSG.edit_image)),
    ),
    Button(Const("🗑 Удалить"), id="delete", on_click=on_delete_company_info),
    Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageCompanyInfoSG.list)),
    state=ManageCompanyInfoSG.company_info_action,
    getter=get_company_info_details,
)


edit_title_window = Window(
    Const("Редактирование названия мероприятия:"),
    Format("Вы хотите изменить название: \n<b>{company_info_title}</b>"),
    TextInput("edit_title", on_success=on_edit_title),
    Cancel(Const("❌ Отмена")),
    state=ManageCompanyInfoSG.edit_title,
    getter=get_company_info_details,
)


edit_description_window = Window(
    Const("Редактирование описания мероприятия:"),
    Format("<b>{company_info_title}</b>"),
    Format("Вы хотите изменить описание: \n{company_info_description}"),
    TextInput("edit_desc", on_success=on_edit_description),
    Cancel(Const("❌ Отмена")),
    state=ManageCompanyInfoSG.edit_description,
    getter=get_company_info_details,
)


edit_file_window = Window(
    Const("📎 Отправьте новый файл (только документ):"),
    MessageInput(on_file_edit),
    Cancel(Const("❌ Отмена")),
    state=ManageCompanyInfoSG.edit_file,
    getter=get_company_info_details,
)

edit_image_window = Window(
    Const("📎 Отправьте новое изображение:"),
    MessageInput(on_image_edit),
    Cancel(Const("❌ Отмена")),
    state=ManageCompanyInfoSG.edit_image,
    getter=get_company_info_details,
)

manage_company_info_dialog = Dialog(
    list_window,
    company_info_detail_window,
    edit_title_window,
    edit_description_window,
    edit_file_window,
    edit_image_window
)
