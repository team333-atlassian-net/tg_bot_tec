import logging
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Button

from dao.auth import create_registration_request, get_users

logger = logging.getLogger(__name__)


class RegisterDialogSG(StatesGroup):
    """
    Состояния диалога регистрации нового пользователя.
    """
    first = State()
    last = State()
    middle = State()
    confirm = State()


# --- Обработчики ввода ---

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

async def get_confirm_data(dialog_manager: DialogManager, **kwargs):
    """
    Подготавливает данные для окна подтверждения.
    """
    return {
        "first_name": dialog_manager.dialog_data.get("first_name", "-"),
        "last_name": dialog_manager.dialog_data.get("last_name", "-"),
        "middle_name": dialog_manager.dialog_data.get("middle_name", "-"),
    }


async def on_confirm(callback: CallbackQuery, button, dialog_manager: DialogManager, **kwargs):
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

    for admin in admins:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Принять", callback_data=f"approve:{request_id}")],
            [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject:{request_id}")],
        ])
        await callback.bot.send_message(
            chat_id=admin.tg_id,
            text=(
                "📥 Новая заявка на регистрацию:\n"
                f"<b>{data['last_name']} {data['first_name']} {data['middle_name']}</b>"
            ),
            reply_markup=kb
        )

    await callback.message.answer("📨 Заявка отправлена. Ожидайте одобрения администратора.")
    logger.info("Пользователь отправил заявку на регистрацию (/register)")
    await dialog_manager.done()


# --- Окна диалога ---

first_name_window = Window(
    Const("👤 Введите ваше имя:"),
    MessageInput(on_first_entered),
    Cancel(Const("❌ Отмена")),
    state=RegisterDialogSG.first,
)

last_name_window = Window(
    Const("👤 Введите вашу фамилию:"),
    MessageInput(on_last_entered),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=RegisterDialogSG.last,
)

middle_name_window = Window(
    Const("👤 Введите ваше отчество:"),
    MessageInput(on_middle_entered),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=RegisterDialogSG.middle,
)

confirm_window = Window(
    Format(
        "🔎 Подтвердите корректность данных:\n\n"
        "👤 Имя: <b>{first_name}</b>\n"
        "👤 Фамилия: <b>{last_name}</b>\n"
        "👤 Отчество: <b>{middle_name}</b>"
    ),
    Row(
        Button(Const("✅ Подтвердить"), id="confirm_register", on_click=on_confirm),
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    state=RegisterDialogSG.confirm,
    getter=get_confirm_data,
)

register_dialog = Dialog(
    first_name_window,
    last_name_window,
    middle_name_window,
    confirm_window,
)
