import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dialogs.faq.add_faq import AddFAQSG
from dialogs.faq.manage_faq import ManageFAQSQ
from dialogs.faq.search_faq import FAQSearchSG
from dialogs.faq.view_faq import FAQSG
from utils.auth import require_admin, require_auth

logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("faq"))
async def show_faq(message: Message, dialog_manager: DialogManager):
    user = await require_auth(message)
    if not user:
        return
    logger.info("Пользователь запросил список вопросов (/faq)")
    await dialog_manager.start(FAQSG.menu, mode=StartMode.RESET_STACK)
    
@router.message(Command("add_faq"))
async def start_add_faq(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.start(AddFAQSG.method, mode=StartMode.RESET_STACK)


@router.message(Command("search_faq"))
async def start_faq_search(message: Message, dialog_manager: DialogManager):
    user = await require_auth(message)
    if not user:
        return
    await dialog_manager.start(FAQSearchSG.search_input)


@router.message(Command("manage_faq"))
async def start_manage_faq(message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.start(ManageFAQSQ.list, mode=StartMode.RESET_STACK)
