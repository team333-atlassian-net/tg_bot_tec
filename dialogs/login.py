from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const
from aiogram.types import Message

from dao.auth import get_user, update_or_add_tg_id

class AuthDialogSG(StatesGroup):
    """Класс состояния для авторизации"""
    enter_pin = State()

async def on_pin_entered(
    message: Message,
    value: str,
    dialog_manager: DialogManager,
    widget 
):
    """Проверяет пин код и авторизует пользователя"""
    tg_id = message.from_user.id
    user = await get_user(pin_code=value.get_value())

    if not user:
        await message.answer("ПИН-код не найден. Повторите команду /login.")
        await dialog_manager.done()
        return

    if user.tg_id and user.tg_id != tg_id:
        await message.answer("Этот ПИН уже использован другим пользователем.")
        await dialog_manager.done()
        return

    await update_or_add_tg_id(user, tg_id) # добавляем tg_id в БД - авторизуем
    await message.answer(f"Добро пожаловать, {user.first_name}!")
    await dialog_manager.done()


login_dialog = Dialog(
    Window(
        Const("Введите ваш ПИН-код для авторизации:"),
        TextInput(id="pin_input", on_success=on_pin_entered),
        state=AuthDialogSG.enter_pin,
    )
)
