from dao.auth import get_user, is_admin
from aiogram.types import Message

async def require_auth(message: Message):
    tg_id = message.from_user.id
    user = await get_user(tg_id=tg_id)

    if not user:
        await message.answer("Вы не авторизованы. Введите пин-код с помощью /login.\nДля регистрации введите /register")
        return

    return user


async def require_admin(message: Message):
    tg_id = message.from_user.id
    user = await get_user(tg_id=tg_id)

    if not user:
        await message.answer("❌ Вы не авторизованы. Введите пин-код с помощью /login.\nДля регистрации введите /register")
        return
    
    if not await is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора.")
        return
    
    return user