from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from dao.company_info import get_company_info_by_id
from states import CompanyInfoViewSG


async def on_company_info_selected(
    callback: CallbackQuery, widget, manager: DialogManager, selected_id: str
):
    """
    Обработчик выбора раздела организационной структуры из списка.
    Сохраняет выбранный раздел, отправляет файл (если есть),
    и переключает диалог на окно детального просмотра.
    """
    company_info = await get_company_info_by_id(int(selected_id))
    manager.dialog_data["company_info"] = company_info
    manager.dialog_data["selected_company_info_id"] = selected_id

    if company_info:
        if company_info.file_path:
            await callback.message.answer_document(company_info.file_path)
        if company_info.image_path:
            await callback.message.answer_photo(company_info.image_path)

    await manager.switch_to(CompanyInfoViewSG.detail)
