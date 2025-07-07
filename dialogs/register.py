import logging
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from dao.auth import create_registration_request, get_users

logger = logging.getLogger(__name__)

class RegisterDialogSG(StatesGroup):
    """Класс состояния регистрации"""
    first = State()
    last = State()
    middle = State()

# --- Обработчики ввода ---
async def on_first_entered(message: Message,
                           value: str,
                           dialog_manager: DialogManager,
                           widget):
    """Обработчик имени"""
    dialog_manager.dialog_data["first_name"] = value.get_value()
    await dialog_manager.switch_to(RegisterDialogSG.last)

async def on_last_entered(message: Message,
                           value: str,
                           dialog_manager: DialogManager,
                           widget):
    """Обработчик фамилии"""
    dialog_manager.dialog_data["last_name"] = value.get_value()
    await dialog_manager.switch_to(RegisterDialogSG.middle)

async def on_middle_entered(message: Message,
                           value: str,
                           dialog_manager: DialogManager,
                           widget):
    """
    Обработчик отчества
    Отправляет заявку на регистрацию админу
    """
    data = dialog_manager.dialog_data
    first_name = data["first_name"]
    last_name = data["last_name"]
    middle_name = value.get_value()
    tg_id = str(message.from_user.id)

    request = await create_registration_request(tg_id, first_name, last_name, middle_name)
    admins = await get_users(admin_rule=True)
    request_id = request.id

    for admin in admins:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Принять", callback_data=f"approve:{request_id}")],
            [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject:{request_id}")]
        ])
        await message.bot.send_message(
            chat_id=admin.tg_id,
            text=f"Новая заявка:\n<b>{last_name} {first_name} {middle_name}</b>",
            reply_markup=kb
        )

    await message.answer("Заявка отправлена. Ожидайте одобрения.")
    logger.info("Пользователь отправил заявку на регистрацию админу (/register)")
    await dialog_manager.done()

# Диалог регистрации
register_dialog = Dialog(
    Window(
        Const("Введите ваше имя:"),
        TextInput(id="first", on_success=on_first_entered),
        state=RegisterDialogSG.first,
    ),
    Window(
        Const("Введите вашу фамилию:"),
        TextInput(id="last", on_success=on_last_entered),
        state=RegisterDialogSG.last,
    ),
    Window(
        Const("Введите ваше отчество:"),
        TextInput(id="middle", on_success=on_middle_entered),
        state=RegisterDialogSG.middle,
    ),
)
