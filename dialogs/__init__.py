from aiogram_dialog import setup_dialogs
from aiogram import Dispatcher

from dialogs.login import login_dialog
from dialogs.register import register_dialog
from dialogs.add_user import add_user_dialog


def register_all_dialogs(dp: Dispatcher):
    setup_dialogs(dp) 
    dp.include_router(login_dialog)
    dp.include_router(register_dialog)
    dp.include_router(add_user_dialog)
