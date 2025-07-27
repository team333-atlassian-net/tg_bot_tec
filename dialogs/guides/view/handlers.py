import logging
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import (
    Select,
)
from states import GuideViewSG

logger = logging.getLogger(__name__)


async def on_doc_select(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["doc"] = manager.dialog_data["docs"][int(selected_id)]
    await manager.switch_to(GuideViewSG.guides)


async def on_guide_select(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["guide_id"] = int(selected_id)
    await manager.switch_to(GuideViewSG.guide)
