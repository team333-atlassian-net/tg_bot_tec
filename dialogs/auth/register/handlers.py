import logging

from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram_dialog import DialogManager

from dao.auth import create_registration_request, get_users
from states import RegisterDialogSG
from dialogs.auth.register.handlers import *
from dialogs.auth.register.getters import *

logger = logging.getLogger(__name__)


async def on_first_entered(message: Message, widget, dialog_manager: DialogManager):
    """
    Обрабатывает ввод имени.
    """
    dialog_manager.dialog_data["first_name"] = message.text
    await dialog_manager.switch_to(RegisterDialogSG.last)


async def on_last_entered(message: Message, widget, dialog_manager: DialogManager):
    """
    Обрабатывает ввод фамилии.
    """
    dialog_manager.dialog_data["last_name"] = message.text
    await dialog_manager.switch_to(RegisterDialogSG.middle)


async def on_middle_entered(message: Message, widget, dialog_manager: DialogManager):
    """
    Обрабатывает ввод отчества.
    Переход к окну подтверждения.
    """
    dialog_manager.dialog_data["middle_name"] = message.text
    await dialog_manager.switch_to(RegisterDialogSG.confirm)


# --- Подтверждение ---


async def on_confirm(
    callback: CallbackQuery, button, dialog_manager: DialogManager, **kwargs
):
    """
    Обрабатывает нажатие кнопки "Подтвердить".
    Отправляет заявку админу.
    """
    data = dialog_manager.dialog_data
    tg_id = str(callback.from_user.id)

    request = await create_registration_request(
        tg_id,
        data["first_name"],
        data["last_name"],
        data["middle_name"],
    )

    admins = await get_users(admin_rule=True)
    request_id = request.id

    valid_admins = [admin for admin in admins if admin.tg_id]

    if not valid_admins:
        await callback.message.answer(
            "К сожалению, сейчас нет доступных администраторов для обработки вашей заявки. "
            "Пожалуйста, попробуйте отправить заявку позже."
        )
        await dialog_manager.done()
        return

    for admin in valid_admins:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Принять", callback_data=f"approve:{request.id}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Отклонить", callback_data=f"reject:{request.id}"
                    )
                ],
            ]
        )
        await callback.bot.send_message(
            chat_id=admin.tg_id,
            text=(
                "📥 Новая заявка на регистрацию:\n"
                f"<b>{data['last_name']} {data['first_name']} {data['middle_name']}</b>"
            ),
            reply_markup=kb,
        )


    await callback.message.answer(
        "📨 Заявка отправлена. Ожидайте одобрения администратора."
    )
    logger.info("Пользователь отправил заявку на регистрацию (/register)")
    await dialog_manager.done()
