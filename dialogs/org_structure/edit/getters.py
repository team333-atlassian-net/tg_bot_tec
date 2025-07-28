import logging

from aiogram_dialog import DialogManager
from dao.org_structure import (
    get_all_org_structures,
    get_org_structure_by_id,
)


logger = logging.getLogger(__name__)


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
        return {
            "org_structure_title": "Неизвестный раздел оргструктуры",
            "org_structure_description": "",
        }
    org_structure = await get_org_structure_by_id(int(org_structure_id))
    if not org_structure:
        return {
            "org_structure_title": "Информация не найдена",
            "org_structure_description": "",
        }
    return {
        "org_structure_title": org_structure.title,
        "org_structure_description": org_structure.content or "-",
    }
