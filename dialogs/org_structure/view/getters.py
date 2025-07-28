from aiogram_dialog import DialogManager

from dao.org_structure import get_all_org_structures, get_org_structure_by_id


async def get_structure_list(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для получения списка всех разделов оргструктуры.
    """
    structures = await get_all_org_structures()
    return {"structures": [(str(s.id), s.title) for s in structures]}


async def get_structure_detail(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для получения подробностей по выбранному разделу.
    """
    structure = dialog_manager.dialog_data.get("structure")
    if not structure:
        structure_id = dialog_manager.dialog_data.get("selected_structure_id")
        if not structure_id:
            return {"structure": None, "content": ""}
        structure = await get_org_structure_by_id(int(structure_id))
        dialog_manager.dialog_data["structure"] = structure

    return {"structure": structure, "content": structure.content or "-"}
