from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from dao.org_structure import get_org_structure_by_id
from states import OrgStructureViewSG


async def on_structure_selected(
    callback: CallbackQuery, widget, manager: DialogManager, selected_id: str
):
    """
    Обработчик выбора раздела организационной структуры из списка.
    Сохраняет выбранный раздел, отправляет файл (если есть),
    и переключает диалог на окно детального просмотра.
    """
    structure = await get_org_structure_by_id(int(selected_id))
    manager.dialog_data["structure"] = structure
    manager.dialog_data["selected_structure_id"] = selected_id

    if structure and structure.file_id:
        await callback.message.answer_document(structure.file_id)

    await manager.switch_to(OrgStructureViewSG.detail)
