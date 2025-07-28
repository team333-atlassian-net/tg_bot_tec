import logging

from aiogram_dialog import DialogManager
from dao.company_info import (
    get_all_company_info,
    get_company_info_by_id,
)

logger = logging.getLogger(__name__)


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
        return {
            "company_info_title": "Неизвестный раздел информации",
            "company_info_description": "",
        }
    company_info = await get_company_info_by_id(int(company_info_id))
    if not company_info:
        return {
            "company_info_title": "Информация не найдена",
            "company_info_description": "",
        }
    return {
        "company_info_title": company_info.title,
        "company_info_description": company_info.content or "-",
    }
