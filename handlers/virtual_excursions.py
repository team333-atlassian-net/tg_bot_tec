from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dao.company_info import get_all_company_info
from dialogs.virtual_excursions import ExcursionCreationSG, ExcursionView
from utils.auth import require_admin, require_auth

router = Router()


@router.message(Command("add_virtual_excursion"))
async def add_virtual_excursion(message: Message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.reset_stack()
    await dialog_manager.start(ExcursionCreationSG.title, mode=StartMode.RESET_STACK)


# @router.message(Command("add_excursion_material"))
# async def add_excursion_material(message: Message, dialog: DialogManager):
#     user = await require_admin(message)
#     if not user:
#         return
#     await dialog.reset_stack()


@router.message(Command("virtual_excursions"))
async def show_virtual_excursions(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ExcursionView.list, mode=StartMode.RESET_STACK)
