from datetime import date

from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Button, ScrollingGroup, Radio, Calendar

from dao.canteen import (
    get_all_canteen_menu,
    get_canteen_menu_by_id,
    get_canteen_info,
)
from models import CanteenMenuFileType

class CanteenViewSG(StatesGroup):
    """Состояния диалога просмотра столовой и меню"""
    start = State()        
    menu_list = State()    
    menu_detail = State()  
    calendar = State()     
    info = State()         


async def get_canteen_menu_list(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает список всех меню для отображения в Radio-кнопках.
    """
    menus = await get_all_canteen_menu()
    return {"canteen_menus": [(str(m.id), m.date.strftime("%Y-%m-%d")) for m in menus]}

async def on_menu_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_id: str):
    """
    Загружает выбранное меню по ID, сохраняет его в dialog_data и отображает файл.
    """
    menu = await get_canteen_menu_by_id(int(selected_id))
    manager.dialog_data["canteen_menu"] = menu
    manager.dialog_data["selected_menu_id"] = selected_id

    # Отправляем файл пользователю в зависимости от его типа
    if menu and menu.file_id:
        if menu.file_type == CanteenMenuFileType.PHOTO:
            await callback.message.answer_photo(menu.file_id)
        else:
            await callback.message.answer_document(menu.file_id)

    await manager.switch_to(CanteenViewSG.menu_detail)

async def get_canteen_menu_detail(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает контент меню для окна с деталями.
    """
    menu = dialog_manager.dialog_data.get("canteen_menu")
    if not menu:
        return {"canteen_menu": None, "content": "", "formatted_date": ""}
    content = menu.menu or "📄 Меню не указано"
    formatted_date = menu.date.strftime("%Y-%m-%d") if menu.date else ""
    return {
        "canteen_menu": menu,
        "content": content,
        "formatted_date": formatted_date,
    }

async def on_date_selected(callback: CallbackQuery, widget, dialog_manager: DialogManager, selected_date: date):
    """
    Ищет меню по выбранной дате, отправляет файл и переходит к окну с деталями.
    """
    menus = await get_all_canteen_menu()
    selected = next((m for m in menus if m.date == selected_date), None)
    if not selected:
        await callback.message.answer("❌ Меню на эту дату не найдено.")
        return

    dialog_manager.dialog_data["canteen_menu"] = selected
    dialog_manager.dialog_data["selected_menu_id"] = selected.id

    if selected.file_id:
        if selected.file_type == CanteenMenuFileType.PHOTO:
            await callback.message.answer_photo(selected.file_id)
        else:
            await callback.message.answer_document(selected.file_id)

    await dialog_manager.switch_to(CanteenViewSG.menu_detail)


async def get_canteen_info_detail(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает текст с расписанием и описанием столовой.
    """
    info = await get_canteen_info()
    if not info:
        return {"content": "Информация о столовой пока не добавлена."}
    return {
        "content": f"⏰ Время работы: {info.start_time.strftime('%H:%M')} - {info.end_time.strftime('%H:%M')}\n\n"
                   f"📝 Описание: {info.description or '—'}"
    }


start_window = Window(
    Const("🍽 Что вы хотите посмотреть?"),
    Row(
        Button(Const("📋 Меню"), id="menu", on_click=lambda c, b, m: m.switch_to(CanteenViewSG.menu_list)),
        Button(Const("🏢 Информация о столовой"), id="info", on_click=lambda c, b, m: m.switch_to(CanteenViewSG.info)),
    ),
    Cancel(Const("❌ Отмена")),
    state=CanteenViewSG.start,
)


menu_list_window = Window(
    Const("📅 Выберите дату меню:"),
    ScrollingGroup(
        Radio(
            checked_text=Format("✅ {item[1]}"),
            unchecked_text=Format("{item[1]}"),
            id="menu_radio",
            item_id_getter=lambda x: x[0],
            items="canteen_menus",
            on_click=on_menu_selected,
        ),
        id="menu_scroll",
        width=1,
        height=5,
    ),
    Row(
        Button(Const("📆 Календарь"), id="calendar", on_click=lambda c, b, m: m.switch_to(CanteenViewSG.calendar)),
        Cancel(Const("❌ Отмена")),
    ),
    state=CanteenViewSG.menu_list,
    getter=get_canteen_menu_list,
)


menu_detail_window = Window(
    Format("📌 <b>Меню на {formatted_date}</b>\n\n{content}"),
    Row(Back(Const("⬅️ Назад")), Cancel(Const("❌ Закрыть"))),
    state=CanteenViewSG.menu_detail,
    getter=get_canteen_menu_detail,
)


calendar_window = Window(
    Const("📆 Выберите дату меню:"),
    Calendar(id="menu_calendar", on_click=on_date_selected),
    Row(Back(Const("⬅️ Назад")), Cancel(Const("❌ Отмена"))),
    state=CanteenViewSG.calendar,
)

canteen_info_window = Window(
    Format("{content}"),
    Row(
        Button(Const("⬅️ Назад"), id="back_to_menu", on_click=lambda c, b, m: m.switch_to(CanteenViewSG.start)),
        Cancel(Const("❌ Закрыть"))
    ),
    state=CanteenViewSG.info,
    getter=get_canteen_info_detail,
)

canteen_dialog = Dialog(
    start_window,
    menu_list_window,
    menu_detail_window,
    calendar_window,
    canteen_info_window,
)
