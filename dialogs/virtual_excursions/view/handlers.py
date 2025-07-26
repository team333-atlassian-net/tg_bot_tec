import logging
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import (
    Select,
)
from states import ExcursionViewSG


async def on_virtex_selected(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["selected_virtex_id"] = int(selected_id)
    await manager.switch_to(ExcursionViewSG.detail)


async def on_material_selected(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["selected_material_id"] = int(selected_id)
    await manager.switch_to(ExcursionViewSG.material)
