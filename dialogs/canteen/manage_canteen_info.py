import logging

from datetime import datetime, date
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Cancel, Row
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.kbd import Calendar, Radio, ScrollingGroup

from dao.canteen import delete_canteen_info, delete_canteen_menu, delete_canteen_menu_file, get_all_canteen_menu, get_canteen_menu_by_date, get_canteen_menu_by_id, update_canteen_info, update_canteen_menu
from dao.canteen import get_canteen_info as dao_get_canteen_info
from models import CanteenMenuFileType

logger = logging.getLogger(__name__)

class ManageCanteenSG(StatesGroup):
    """
    Состояния для управления меню и информацией о столовой.
    """
    choice = State()
    select_menu = State()
    menu_edit_action = State()
    edit_menu_text = State()
    edit_menu_file = State()
    confirm_menu_edit = State()
    confirm_info = State()

    edit_canteen_info = State()
    canteen_info_action = State()
    edit_info = State()
    edit_description = State()
    edit_start_time = State()
    edit_end_time = State()

# геттеры

async def get_canteen_info(dialog_manager: DialogManager, **kwargs):
    """
    Получает и возвращает текущее описание столовой и время работы.
    Используется в качестве getter для окон.
    """
    canteen = await dao_get_canteen_info()
    return {
        "start_time": canteen.start_time,
        "end_time": canteen.end_time,
        "description": canteen.description or "-",
    }

async def get_menu_dates(dialog_manager: DialogManager, **kwargs):
    menus = await get_all_canteen_menu()
    return {
        "canteen_menus": [(str(m.id), m.date.strftime("%Y-%m-%d")) for m in menus[:5]]
    }


async def get_selected_menu(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает выбранное меню для отображения содержимого и даты.
    """
    menu = dialog_manager.dialog_data.get("selected_menu")
    if not menu:
        return {"content": "", "formatted_date": ""}
    return {
        "content": menu.menu or "-",
        "formatted_date": menu.date.strftime("%Y-%m-%d"),
    }

# обработчики действий

async def on_edit_start_time_start(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Переходит к окну ввода нового времени начала работы столовой.
    """
    await dialog_manager.switch_to(ManageCanteenSG.edit_start_time)

async def on_edit_start_time(message: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Сохраняет новое время начала работы столовой.
    """
    start_time_text = value.get_value()
    try:
        time = datetime.strptime(start_time_text, "%H:%M").time()
    except ValueError:
        await message.answer("❌ Неверный формат времени. Введите в формате HH:MM, например: 10:00")
        return

    await update_canteen_info(start=time, end=None, description=None)
    await message.answer("✏️ Время начала работы столовой обновлено.")
    logger.info("Администратор обновил время начала работы столовой (/manage_canteen_info)")
    await dialog_manager.switch_to(ManageCanteenSG.canteen_info_action)

async def on_edit_end_time_start(callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs):
    """
    Переход к окну редактирования времени окончания работы.
    """
    await dialog_manager.switch_to(ManageCanteenSG.edit_end_time)

async def on_edit_end_time(message: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Сохраняет новое время окончания работы столовой.
    """
    end_time_text = value.get_value()
    try:
        time = datetime.strptime(end_time_text, "%H:%M").time()
    except ValueError:
        await message.answer("❌ Неверный формат времени. Введите в формате HH:MM, например: 16:00")
        return

    await update_canteen_info(start=None, end=time, description=None)
    await message.answer("✏️ Время завершения работы столовой обновлено.")
    logger.info("Администратор обновил время авершения работы столовой (/manage_canteen_info)")
    await dialog_manager.switch_to(ManageCanteenSG.canteen_info_action)

async def on_edit_description(message: Message, value: TextInput, dialog_manager: DialogManager, widget):
    """
    Обновляет описание столовой.
    """
    await update_canteen_info(None, None, value.get_value())
    await message.answer("✏️ Описание столовой обновлено.")
    logger.info("Администратор обновил описание столовой (/manage_canteen_info)")
    await dialog_manager.switch_to(ManageCanteenSG.canteen_info_action)

async def on_delete_canteen_info(callback: CallbackQuery, widget, dialog_manager: DialogManager):
    """
    Удаляет всю информацию о столовой.
    """
    await delete_canteen_info()
    await callback.message.answer("❌ Информация о столовой удалена.")
    logger.info("Администратор удалил информацию о столовой (/manage_canteen_info)")
    await dialog_manager.switch_to(ManageCanteenSG.choice)

async def on_select_menu(callback: CallbackQuery, widget, dialog_manager: DialogManager, selected_id: str):
    """
    Обработка выбора меню по ID из списка.
    """
    menu = await get_canteen_menu_by_id(int(selected_id))
    dialog_manager.dialog_data["selected_menu"] = menu
    dialog_manager.dialog_data["menu_id"] = menu.id
    await dialog_manager.switch_to(ManageCanteenSG.menu_edit_action)

async def on_select_menu_by_date(callback: CallbackQuery, widget, dialog_manager: DialogManager, selected_date: date):
    """
    Обработка выбора меню по дате (из календаря).
    """
    menu = await get_canteen_menu_by_date(selected_date)
    if not menu:
        await callback.message.answer("❌ На выбранную дату меню не найдено.")
        return
    dialog_manager.dialog_data["selected_menu"] = menu
    dialog_manager.dialog_data["menu_id"] = menu.id
    await dialog_manager.switch_to(ManageCanteenSG.menu_edit_action)

async def on_edit_menu_text(message: Message, input: TextInput, dialog_manager: DialogManager, widget):
    """
    Обновляет текст меню.
    """
    new_text = input.get_value()
    menu_id = dialog_manager.dialog_data.get("menu_id")
    await update_canteen_menu(menu_id, None, new_text, None, None)

    updated_menu = await get_canteen_menu_by_id(menu_id)
    dialog_manager.dialog_data["selected_menu"] = updated_menu

    await message.answer("✏️ Текст меню обновлён.")
    logger.info("Администратор обновил меню столовой (/manage_canteen_info)")
    await dialog_manager.switch_to(ManageCanteenSG.menu_edit_action)

async def on_edit_menu_file(message: Message, widget, dialog_manager: DialogManager):
    """
    Обновляет файл (документ/изображение) для выбранного меню.
    """
    if not message.document and not message.photo:
        await message.answer("❌ Пришлите файл (документ или изображение).")
        return

    file_id = None
    file_type = None
    if message.document:
        file_id = message.document.file_id
        file_type = CanteenMenuFileType.FILE
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_type = CanteenMenuFileType.PHOTO

    menu_id = dialog_manager.dialog_data.get("menu_id")
    await update_canteen_menu(menu_id, None, None, file_id=file_id, file_type=file_type)
    updated_menu = await get_canteen_menu_by_id(menu_id)
    dialog_manager.dialog_data["selected_menu"] = updated_menu

    await message.answer("📎 Файл меню обновлён.")
    logger.info("Администратор обновил файл меню столовой (/manage_canteen_info)")
    await dialog_manager.switch_to(ManageCanteenSG.menu_edit_action)

async def on_delete_menu_file(callback: CallbackQuery, widget, dialog_manager: DialogManager):
    """
    Удаляет прикреплённый файл у выбранного меню.
    """
    menu_id = dialog_manager.dialog_data.get("menu_id")
    await delete_canteen_menu_file(menu_id)
    updated_menu = await get_canteen_menu_by_id(menu_id)
    dialog_manager.dialog_data["selected_menu"] = updated_menu

    await callback.message.answer("🗑 Файл меню удалён.")
    await dialog_manager.show()


async def on_delete_menu(callback: CallbackQuery, widget, dialog_manager: DialogManager):
    """
    Удаляет выбранное меню.
    """
    menu_id = dialog_manager.dialog_data.get("menu_id")
    if not menu_id:
        await callback.message.answer("❌ Меню не выбрано.")
        return

    await delete_canteen_menu(menu_id)
    await callback.message.answer("🗑 Меню удалено.")
    logger.info(f"Администратор удалил меню с id={menu_id} (/manage_canteen_info)")
    await dialog_manager.switch_to(ManageCanteenSG.select_menu) 

    
edit_choice_window = Window(
    Const("Что хотите отредактировать?"),
    Row(
        Button(
            Const("✏️ Информация о столовой"),
            id="edit_info",
            on_click=lambda c, b, m: m.switch_to(ManageCanteenSG.canteen_info_action)),
        Button(
            Const("✏️ Меню"),
            id="edit_menu",
            on_click=lambda c, b, m: m.switch_to(ManageCanteenSG.select_menu)
            ),
    ),
    Cancel(Const("❌ Отмена")),
    state=ManageCanteenSG.choice,
)

canteen_info_detail_window = Window(
    Const("Выберите действие с информацией:"),
    Format("<b>Время начала работы: </b>{start_time}"),
    Format("<b>Время завершения работы: </b>{end_time}"),
    Format("{description}"),
    Row(
        Button(
            Const("✏️ Время начала работы"),
            id="edit_start_time",
            on_click=on_edit_start_time_start
            ),
        Button(
            Const("✏️ Время завершения работы"),
            id="edit_end_time",
            on_click=on_edit_end_time_start
            ),
    ),
    Row(
        Button(
            Const("✏️ Описание"),
            id="edit_file",
            on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.edit_description)
            ),
        Button(
            Const("🗑 Удалить"),
            id="delete",
            on_click=on_delete_canteen_info
            ),
        ),
    Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.choice)),
    state=ManageCanteenSG.canteen_info_action,
    getter=get_canteen_info,
)

edit_start_time_window = Window(
    Const("Редактирование время начала работы столовой:"),
    Format("Вы хотите изменить время: \n<b>{start_time}</b>"),
    TextInput("edit_start_time", on_success=on_edit_start_time),
    Row(
        Cancel(Const("❌ Отмена")),
        Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.canteen_info_action)),
    ),
    state=ManageCanteenSG.edit_start_time,
    getter=get_canteen_info,
)

edit_end_time_window = Window(
    Const("Редактирование время завершения работы столовой:"),
    Format("Вы хотите изменить время: \n<b>{end_time}</b>"),
    TextInput("edit_end_time", on_success=on_edit_end_time),
    Row(
        Cancel(Const("❌ Отмена")),
        Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.canteen_info_action)),
    ),
    state=ManageCanteenSG.edit_end_time,
    getter=get_canteen_info,
)

edit_description_window = Window(
    Const("Редактирование описание столовой:"),
    Format("<b>Время начала работы: </b>{start_time}"),
    Format("<b>Время завершения работы: </b>{end_time}"),
    Format("Вы хотите отредактировать описание: \n{description}"),
    TextInput("edit_description", on_success=on_edit_description),
    Row(
        Cancel(Const("❌ Отмена")),
        Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.canteen_info_action)),
    ),
    state=ManageCanteenSG.edit_description,
    getter=get_canteen_info,
)
select_menu_window = Window(
    Const("📅 Выберите дату меню для редактирования:"),
    ScrollingGroup(
        Radio(
            checked_text=Format(" {item[1]}"),
            unchecked_text=Format("{item[1]}"),
            id="menu_radio_admin",
            item_id_getter=lambda x: x[0],
            items="canteen_menus",
            on_click=on_select_menu,
        ),
        id="menu_scroll_admin",
        width=1,
        height=5,
    ),
    Row(
        Button(Const("📆 Календарь"), id="calendar_select", on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.confirm_menu_edit)),
        Cancel(Const("❌ Отмена")),
    ),
    state=ManageCanteenSG.select_menu,
    getter=get_menu_dates,
)

calendar_select_window = Window(
    Const("📆 Выберите дату:"),
    Calendar(id="admin_calendar", on_click=on_select_menu_by_date),
    Row(
        Cancel(Const("❌ Отмена")),
        Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.select_menu)),
    ),
    state=ManageCanteenSG.confirm_menu_edit,
)

menu_edit_action_window = Window(
    Format("📌 <b>Меню на {formatted_date}</b>\n\n{content}"),
    Row(
        Button(Const("✏️ Редактировать текст"), id="edit_text", on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.edit_menu_text)),
        Button(Const("📎 Заменить файл"), id="edit_file", on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.edit_menu_file)),
    ),
    Row(
        Button(Const("🗑 Удалить файл"), id="delete_file", on_click=on_delete_menu_file),
                Button(Const("🗑 Удалить меню"), id="delete_menu", on_click=on_delete_menu),),
    Row(
        Cancel(Const("❌ Отмена")),
        Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.select_menu)),
    ),
    state=ManageCanteenSG.menu_edit_action,
    getter=get_selected_menu,
)

edit_menu_text_window = Window(
    Format("Редактирование меню на {formatted_date}:"),
    Format("Вы хотите изменить меню: \n<b>{content}</b>"),
    TextInput(id="menu_text_input", on_success=on_edit_menu_text),
    Row(Cancel(Const("❌ Отмена")),
        Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.menu_edit_action))),
    state=ManageCanteenSG.edit_menu_text,
    getter=get_selected_menu
)

edit_menu_file_window = Window(
    Format("Редактирование меню на {formatted_date}:"),
    Const("📎 Пришлите новый файл меню (фото или документ):"),
    MessageInput(on_edit_menu_file),
    Row(Cancel(Const("❌ Отмена")), Button(Const("⬅️ Назад"), id="back", on_click=lambda c, w, d, **k: d.switch_to(ManageCanteenSG.menu_edit_action))),
    state=ManageCanteenSG.edit_menu_file,
    getter=get_selected_menu
)


manage_canteen_dialog = Dialog(
    edit_choice_window,
    canteen_info_detail_window,
    edit_start_time_window,
    edit_end_time_window,
    edit_description_window,
    select_menu_window,
    calendar_select_window,
    menu_edit_action_window,
    edit_menu_text_window,
    edit_menu_file_window,
)
