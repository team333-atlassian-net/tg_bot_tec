from aiogram_dialog import setup_dialogs
from aiogram import Dispatcher

from dialogs.login import login_dialog
from dialogs.register import register_dialog
from dialogs.add_user import add_user_dialog
from dialogs.admin_events import admin_event_dialog
from dialogs.manage_events import manage_event_dialog
from dialogs.company_info import add_company_info_dialog


def register_all_dialogs(dp: Dispatcher):
    setup_dialogs(dp) 
    dp.include_router(login_dialog)
    dp.include_router(register_dialog)
    dp.include_router(add_user_dialog)
    dp.include_router(admin_event_dialog)
    dp.include_router(manage_event_dialog)
    dp.include_router(add_company_info_dialog)

