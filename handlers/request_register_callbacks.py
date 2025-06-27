from aiogram import Router, F
from aiogram.types import CallbackQuery
from dao.auth import (
    add_user,
    get_request,
    update_request_status,
)
from models import User
from utils.generate_pin import generate_unique_pin

router = Router()


@router.callback_query(F.data.startswith("approve:"))
async def approve_request(callback: CallbackQuery):
    """Подтверждение заявки"""

    request_id = callback.data.split(":")[1]
    request = await get_request(id=request_id)
    pin = await generate_unique_pin()

    await update_request_status(request_id=request_id, status="approved")
    user = User(first_name=request.first_name,
                last_name=request.last_name,
                middle_name=request.middle_name,
                pin_code=pin,
                tg_id=None,
                admin_rule=False)
    await add_user(user)

    await callback.message.bot.send_message(
        chat_id=int(request.tg_id),
        text=f"Ваша заявка одобрена. Ваш ПИН: <b>{pin}</b>"
    )
    await callback.message.answer(
        text=f"👤 Пользователь <b>{request.last_name} {request.first_name}</b> успешно зарегистрирован.\n"
             f"Ему отправлен ПИН-код: <b>{pin}</b>"
    )
    await callback.answer("Пользователь добавлен.")


@router.callback_query(F.data.startswith("reject:"))
async def reject_request(callback: CallbackQuery):
    """Отклонение заявки"""

    request_id = callback.data.split(":")[1]
    request = await get_request(id=request_id)

    await update_request_status(request_id=request_id, status="rejected")
    await callback.message.bot.send_message(
        chat_id=int(request.tg_id),
        text="Ваша заявка отклонена."
    )
    await callback.message.answer(
        text=f"Заявка от <b>{request.last_name} {request.first_name}</b> была отклонена."
    )
    await callback.answer("Заявка отклонена.")
