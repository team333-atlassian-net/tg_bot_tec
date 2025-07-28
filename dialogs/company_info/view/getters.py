from aiogram_dialog import DialogManager

from dao.company_info import get_all_company_info, get_company_info_by_id


async def get_company_info_list(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для получения списка всех разделов.
    """
    company_info = await get_all_company_info()
    return {"company_info": [(str(c.id), c.title) for c in company_info]}


async def get_company_info_detail(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для получения подробностей по выбранному разделу.
    """
    company_info = dialog_manager.dialog_data.get("company_info")
    if not company_info:
        company_info_id = dialog_manager.dialog_data.get("selected_company_info_id")
        if not company_info_id:
            return {"company_info": None, "content": ""}
        company_info = await get_company_info_by_id(int(company_info_id))
        dialog_manager.dialog_data["company_info"] = company_info

    return {"company_info": company_info, "content": company_info.content or "-"}
