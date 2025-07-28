import logging
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import (
    Select, Button,
)
from states import MenuSG

logger = logging.getLogger(__name__)

async def on_auth_click(callback, widget: Button, manager: DialogManager):
    await manager.switch_to(MenuSG.auth)

async def on_info_click(callback, widget: Button, manager: DialogManager):
    await manager.switch_to(MenuSG.company_info)

async def on_canteen_click(callback, widget: Button, manager: DialogManager):
    await manager.switch_to(MenuSG.canteen)

async def on_excursion_click(callback, widget: Button, manager: DialogManager):
    await manager.switch_to(MenuSG.virtexs)

async def on_guide_click(callback, widget: Button, manager: DialogManager):
    await manager.switch_to(MenuSG.guides)

async def on_feedback_click(callback, widget: Button, manager: DialogManager):
    await manager.switch_to(MenuSG.feedback)

async def on_events_click(callback, widget: Button, manager: DialogManager):
    await manager.switch_to(MenuSG.events)

async def on_org_structure_click(callback, widget: Button, manager: DialogManager):
    await manager.switch_to(MenuSG.org_structure)

async def on_faq_click(callback, widget: Button, manager: DialogManager):
    await manager.switch_to(MenuSG.faq)
