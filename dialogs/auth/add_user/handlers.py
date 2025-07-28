import logging
import io
import pandas as pd

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput

from dao.auth import add_user, add_user_with_excel
from models import User
from utils.generate_pin import generate_unique_pin
from utils.auth import require_admin
from states import AddUserSG

logger = logging.getLogger(__name__)

# --- Обработчики ручного ввода ---


async def on_manual_chosen(callback: CallbackQuery, button, manager: DialogManager):
    manager.dialog_data["is_admin"] = False
    await manager.switch_to(AddUserSG.first_name)


async def on_manual_admin_chosen(
    callback: CallbackQuery, button, manager: DialogManager
):
    manager.dialog_data["is_admin"] = True
    await manager.switch_to(AddUserSG.first_name)


async def on_first_name_entered(
    message: Message, widget: TextInput, dialog_manager: DialogManager
):
    dialog_manager.dialog_data["first_name"] = message.text
    await dialog_manager.switch_to(AddUserSG.last_name)


async def on_last_name_entered(
    message: Message, widget: TextInput, dialog_manager: DialogManager
):
    dialog_manager.dialog_data["last_name"] = message.text
    await dialog_manager.switch_to(AddUserSG.middle_name)


async def on_middle_name_entered(
    message: Message, widget: TextInput, dialog_manager: DialogManager
):
    dialog_manager.dialog_data["middle_name"] = message.text
    await dialog_manager.switch_to(AddUserSG.confirm)


async def on_manual_confirm(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, **kwargs
):
    data = dialog_manager.dialog_data
    pin = await generate_unique_pin()
    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        middle_name=data["middle_name"],
        pin_code=pin,
        tg_id=None,
        admin_rule=data.get("is_admin", False),
    )
    await add_user(user)
    status = "администратор" if user.admin_rule else "пользователь"
    await callback.message.answer(
        f"✅ {status.capitalize()} добавлен.\n📌 PIN-код: <b>{pin}</b>"
    )
    logger.info("Администратор зарегистрировал пользователя вручную (/add_user)")
    await dialog_manager.done()


# --- Обработчики Excel ---


async def on_excel_chosen(callback: CallbackQuery, button, manager: DialogManager):
    await manager.switch_to(AddUserSG.upload_excel)


async def on_excel_uploaded(message: Message, widget, dialog_manager: DialogManager):
    user = await require_admin(message)
    if not user:
        return

    file = message.document
    if not file.file_name.endswith(".xlsx"):
        await message.answer("❌ Пожалуйста, отправьте Excel-файл с расширением .xlsx")
        return

    file_bytes = await message.bot.download(file)
    df = pd.read_excel(io.BytesIO(file_bytes.read()))
    required_columns = {"first_name", "last_name", "middle_name"}

    if not required_columns.issubset(df.columns):
        await message.answer(
            "❌ В Excel-файле должны быть колонки: first_name, last_name, middle_name"
        )
        return

    added_users = await add_user_with_excel(df)
    if added_users:
        pin_messages = "\n".join(
            [
                f"🔐 Пин-код для пользователя <b>{full_name}</b>: <code>{pin}</code>"
                for full_name, pin in added_users
            ]
        )
        await message.answer(
            f"✅ Загружено {len(added_users)} пользователей.\n\n{pin_messages}\n\n📌 Передайте PIN-коды пользователям."
        )
    else:
        await message.answer("⚠️ Ни один пользователь не был добавлен.")
    logger.info(
        "Администратор зарегистрировал пользователей с помощью Excel (/add_user)"
    )
    await dialog_manager.done()
