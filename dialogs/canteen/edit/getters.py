import logging

from aiogram_dialog import DialogManager

from dao.canteen import get_all_canteen_menu
from dao.canteen import get_canteen_info as dao_get_canteen_info


logger = logging.getLogger(__name__)


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
