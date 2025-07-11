from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, ScrollingGroup, Radio

from dao.org_structure import get_all_org_structures, get_org_structure_by_id


class OrgStructureViewSG(StatesGroup):
    """
    Состояния для просмотра организационной структуры.
    """
    list = State()
    detail = State()


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

    content = structure.content if structure and structure.content else ""
    return {"structure": structure, "content": content}


async def on_structure_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_id: str):
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


# --- Окна ---

structure_list_window = Window(
    Const("🏢 Выберите раздел организационной структуры:"),
    ScrollingGroup(
        Radio(
            checked_text=Format("{item[1]}"),
            unchecked_text=Format("{item[1]}"),
            id="structure_radio",
            item_id_getter=lambda x: x[0],
            items="structures",
            on_click=on_structure_selected,
        ),
        id="structure_scroll",
        width=1,
        height=3,
    ),
    Cancel(Const("❌ Отмена")),
    state=OrgStructureViewSG.list,
    getter=get_structure_list,
)

structure_detail_window = Window(
    Format("📌 <b>{structure.title}</b>\n\n{content}"),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Закрыть")),
    ),
    state=OrgStructureViewSG.detail,
    getter=get_structure_detail,
)

org_structure_dialog = Dialog(
    structure_list_window,
    structure_detail_window,
)
