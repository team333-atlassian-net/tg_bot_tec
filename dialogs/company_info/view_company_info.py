from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, ScrollingGroup, Radio

from dao.company_info import get_all_company_info, get_company_info_by_id

class CompanyInfoViewSG(StatesGroup):
    """
    Состояния для просмотра организационной структуры.
    """
    list = State()
    detail = State()


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


async def on_company_info_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_id: str):
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


# --- Окна ---

structure_list_window = Window(
    Const("🏢 Выберите раздел:"),
    ScrollingGroup(
        Radio(
            checked_text=Format("{item[1]}"),
            unchecked_text=Format("{item[1]}"),
            id="company_info_radio",
            item_id_getter=lambda x: x[0],
            items="company_info",
            on_click=on_company_info_selected,
        ),
        id="structure_scroll",
        width=1,
        height=5,
    ),
    Cancel(Const("❌ Отмена")),
    state=CompanyInfoViewSG.list,
    getter=get_company_info_list,
)

structure_detail_window = Window(
    Format("📌 <b>{company_info.title}</b>\n\n{content}"),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Закрыть")),
    ),
    state=CompanyInfoViewSG.detail,
    getter=get_company_info_detail,
)

company_info_dialog = Dialog(
    structure_list_window,
    structure_detail_window,
)
