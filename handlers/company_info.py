import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from aiogram.types import Message

from states import CompanyInfoCreationSG, ManageCompanyInfoSG, CompanyInfoViewSG
from utils.auth import require_admin, require_auth

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("company_info"))
async def show_virtual_excursions(message: Message, dialog_manager: DialogManager):
    user = await require_auth(message)
    if not user:
        return
    await dialog_manager.reset_stack()
    logger.info("Пользователь запросил информацию о компании (/company_info)")
    await dialog_manager.start(CompanyInfoViewSG.list, mode=StartMode.RESET_STACK)


@router.message(Command("add_company_info"))
async def start_add_company_info(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.reset_stack()
    await dialog_manager.start(CompanyInfoCreationSG.title, mode=StartMode.RESET_STACK)


@router.message(Command("manage_company_info"))
async def start_manage_events(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.reset_stack()
    await dialog_manager.start(ManageCompanyInfoSG.list, mode=StartMode.RESET_STACK)
