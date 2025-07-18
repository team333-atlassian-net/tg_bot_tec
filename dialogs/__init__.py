from aiogram_dialog import setup_dialogs
from aiogram import Dispatcher

from dialogs.auth.login import login_dialog
from dialogs.auth.register import register_dialog
from dialogs.auth.add_user import add_user_dialog

from dialogs.events.view_events import view_event_dialog
from dialogs.events.manage_events import manage_event_dialog
from dialogs.events.add_event import create_event_dialog

from dialogs.org_structure.add_org_structure import create_org_structure_dialog
from dialogs.org_structure.view_org_structure import org_structure_dialog
from dialogs.org_structure.manage_org_structure import manage_org_structure_dialog

from dialogs.company_info.add_company_info import create_company_info_dialog
from dialogs.company_info.view_company_info import company_info_dialog
from dialogs.company_info.manage_view_company import manage_company_info_dialog

from dialogs.faq.add_faq import add_faq_dialog
from dialogs.faq.view_faq import faq_dialog
from dialogs.faq.search_faq import faq_search_dialog
from dialogs.faq.manage_faq import manage_faq_dialog

from dialogs.canteen.add_canteen_info import add_canteen_info_dialog
from dialogs.canteen.view_canteen_info import canteen_dialog
from dialogs.canteen.manage_canteen_info import manage_canteen_dialog
def register_all_dialogs(dp: Dispatcher):
    setup_dialogs(dp) 
    dp.include_router(login_dialog)
    dp.include_router(register_dialog)
    dp.include_router(add_user_dialog)
    dp.include_router(view_event_dialog)
    dp.include_router(manage_event_dialog)
    dp.include_router(create_event_dialog)
    dp.include_router(create_org_structure_dialog)
    dp.include_router(manage_org_structure_dialog)
    dp.include_router(org_structure_dialog)
    dp.include_router(create_company_info_dialog)
    dp.include_router(company_info_dialog)
    dp.include_router(manage_company_info_dialog)
    dp.include_router(add_faq_dialog)
    dp.include_router(faq_dialog)
    dp.include_router(faq_search_dialog)
    dp.include_router(manage_faq_dialog)
    dp.include_router(add_canteen_info_dialog)
    dp.include_router(canteen_dialog)
    dp.include_router(manage_canteen_dialog)

