from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from aiogram.types import Message

from dialogs.org_structure.add_org_structure import OrgStructureCreationSG
from dialogs.org_structure.view_org_structure import OrgStructureViewSG
from utils.auth import require_admin, require_auth

router = Router()

@router.message(Command("org_structure"))
async def show_virtual_excursions(message: Message, dialog_manager: DialogManager):
    user = await require_auth(message)
    if not user:
        return
    await dialog_manager.reset_stack()
    await dialog_manager.start(OrgStructureViewSG.list, mode=StartMode.RESET_STACK)


@router.message(Command("add_org_structure"))
async def start_add_event(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.reset_stack()
    await dialog_manager.start(OrgStructureCreationSG.title, mode=StartMode.RESET_STACK)


# @router.message(Command("manage_org_structure"))
# async def start_manage_events(message, dialog_manager: DialogManager):
#     user = await require_admin(message)
#     if not user:
#         return
#     await dialog_manager.reset_stack()
#     await dialog_manager.start(ManageEventSG.list, mode=StartMode.RESET_STACK)