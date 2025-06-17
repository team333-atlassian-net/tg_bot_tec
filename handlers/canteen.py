from aiogram import Router, F
from aiogram.types import Message, InputFile
from dao.auth import get_user
from dao.canteen import get_latest_canteen_info

router = Router()

@router.message(F.text.lower() == "столовая")
async def canteen_info_handler(message: Message):
    """Хэндлер на получение информации о столовой"""
    # проверка, что пользователь авторизован
    tg_id = message.from_user.id
    user = await get_user(tg_id=tg_id)
    if not user:
        await message.answer("Вы не авторизованы. Введите пин-код с помощью /login.")
        return
    
    canteen_info = await get_latest_canteen_info()

    if not canteen_info:
        await message.answer("Информация о столовой пока не добавлена.")
        return

    text = (
        f"🕒 *Режим работы:*\n{canteen_info.work_schedule}\n\n"
        f"📋 *Меню:*\n{canteen_info.menu_text}"
    )

    await message.answer(text, parse_mode="Markdown")

    # Отправка файла (если есть)
    if canteen_info.file_path:
        try:
            await message.answer_document(InputFile(canteen_info.file_path))
        except Exception as e:
            await message.answer(f"⚠️ Не удалось отправить файл меню: {e}")

    # Отправка изображения (если есть)
    if canteen_info.image_path:
        try:
            await message.answer_photo(InputFile(canteen_info.image_path))
        except Exception as e:
            await message.answer(f"⚠️ Не удалось отправить изображение: {e}")
