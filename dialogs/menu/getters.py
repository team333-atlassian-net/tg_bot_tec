from aiogram.types import Message, User
from aiogram_dialog import DialogManager

from models import User as BotUser
from utils.auth import require_auth


async def auth_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    user: BotUser = await require_auth(event_from_user)  # проверка, что пользователь авторизован

    not_auth_text = "Вы не авторизованы. Войдите в систему или зарегистрируйтесь"
    auth_text = "Выберите интересующий Вас модуль"

    return {"not_auth_text": not_auth_text,
            "auth_text": auth_text,
            "is_not_auth": not user,
            "is_auth": user}


async def role_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    user: BotUser = await require_auth(event_from_user)  # проверка, что пользователь авторизован

    return {
        "is_admin": user.admin_rule if user else False,
    }
