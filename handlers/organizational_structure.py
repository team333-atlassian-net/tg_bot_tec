from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dao.organizational_structure import get_all_organizational_structure
from dialogs.organizational_structure import AddOrganizationalStructureSG
from utils.auth import require_admin, require_auth

router = Router()

@router.message(Command("add_org_structure"))
async def start_add_info(message: Message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.reset_stack()
    await dialog_manager.start(AddOrganizationalStructureSG.title, mode=StartMode.RESET_STACK)

@router.message(Command("org_structure"))
async def show_company_info(message: Message):
    user = await require_auth(message)
    if not user:
        return
    infos = await get_all_organizational_structure()
    if not infos:
        await message.answer("ℹ️ Пока нет информации об организационной структуре компании.")
        return

    for info in infos:
        text = f"🏢 <b>{info.title}</b>"
        if info.content:
            text += f"\n\n{info.content}"

        if info.file_id:
            await message.bot.send_document(
                chat_id=message.chat.id,
                document=info.file_id,
                caption=text,
                parse_mode="HTML",
            )
        else:
            await message.answer(text, parse_mode="HTML")
