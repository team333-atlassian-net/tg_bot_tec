from aiogram_dialog import setup_dialogs
from aiogram import Dispatcher

from dialogs.login import login_dialog
from dialogs.register import register_dialog
from dialogs.add_user import add_user_dialog
from dialogs.admin_events import admin_event_dialog
from dialogs.manage_events import manage_event_dialog
from dialogs.company_info import add_company_info_dialog
from dialogs.org_structure.add_org_structure import create_org_structure_dialog
from dialogs.org_structure.view_org_structure import org_structure_dialog


def register_all_dialogs(dp: Dispatcher):
    setup_dialogs(dp) 
    dp.include_router(login_dialog)
    dp.include_router(register_dialog)
    dp.include_router(add_user_dialog)
    dp.include_router(admin_event_dialog)
    dp.include_router(manage_event_dialog)
    dp.include_router(add_company_info_dialog)
    dp.include_router(create_org_structure_dialog)
    dp.include_router(org_structure_dialog)

