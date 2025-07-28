from datetime import date

from aiogram_dialog import DialogManager

from dao.canteen import (
    get_canteen_info,
    get_canteen_menu_by_week,
)


async def get_canteen_menu_list(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает список всех меню для отображения в Radio-кнопках.
    """
    menus = await get_canteen_menu_by_week()
    return {"canteen_menus": [(str(m.id), m.date.strftime("%Y-%m-%d")) for m in menus]}


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


async def get_canteen_info_detail(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает текст с расписанием и описанием столовой.
    """
    info = await get_canteen_info()
    if not info:
        return {"content": "Информация о столовой пока не добавлена."}
    return {
        "content": f"⏰ Время работы: {info.start_time.strftime('%H:%M')} - {info.end_time.strftime('%H:%M')}\n\n"
        f"📝 Описание: {info.description or '-'}"
    }
