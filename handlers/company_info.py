from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dao.company_info import get_all_company_info
from dialogs.company_info import AddCompanyInfoSG
from utils.auth import require_admin, require_auth

router = Router()

@router.message(Command("add_company_info"))
async def start_add_info(message: Message, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return
    await dialog_manager.reset_stack()
    await dialog_manager.start(AddCompanyInfoSG.title, mode=StartMode.RESET_STACK)

@router.message(Command("company_info"))
async def show_company_info(message: Message):
    user = await require_auth(message)
    if not user:
        return
    infos = await get_all_company_info()
    if not infos:
        await message.answer("ℹ️ Пока нет информации о компании.")
        return

    for info in infos:
        text = f"🏢 <b>{info.title}</b>"
        if info.content:
            text += f"\n\n{info.content}"

        # если есть изображение — отправляем его с подписью
        if info.image_path:
            await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=info.image_path,
                caption=text,
                parse_mode="HTML",
            )
            # Отдельно добавляем файл, если есть
            if info.file_path:
                await message.bot.send_document(
                    chat_id=message.chat.id,
                    document=info.file_path
                )
        elif info.file_path:
            await message.bot.send_document(
                chat_id=message.chat.id,
                document=info.file_path,
                caption=text,
                parse_mode="HTML",
            )
        else:
            # Ни изображения, ни файла — просто текст
            await message.answer(text, parse_mode="HTML")
