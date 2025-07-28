from aiogram_dialog import setup_dialogs
from aiogram import Dispatcher

from dialogs.auth.login.dialog import dialog as login_dialog
from dialogs.auth.register.dialog import dialog as register_dialog
from dialogs.auth.add_user.dialog import dialog as add_user_dialog

from dialogs.virtual_excursions.create.dialog import dialog as create_virtex_dialog
from dialogs.virtual_excursions.view.dialog import dialog as virtex_dialog
from dialogs.virtual_excursions.edit.dialog import dialog as edit_virtex_dialog

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

from dialogs.guides.view.dialog import dialog as guides_dialog
from dialogs.guides.create.dialog import dialog as add_guide_dialog
from dialogs.guides.edit.dialog import dialog as manage_guides_dialog

from dialogs.feedback.user.dialog import dialog as user_feedback_dialog
from dialogs.feedback.admin.dialog import dialog as admin_feedback_dialog


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
    dp.include_router(create_virtex_dialog)
    dp.include_router(virtex_dialog)
    dp.include_router(edit_virtex_dialog)
    dp.include_router(company_info_dialog)
    dp.include_router(manage_company_info_dialog)
    dp.include_router(add_faq_dialog)
    dp.include_router(faq_dialog)
    dp.include_router(faq_search_dialog)
    dp.include_router(manage_faq_dialog)
    dp.include_router(add_canteen_info_dialog)
    dp.include_router(canteen_dialog)
    dp.include_router(manage_canteen_dialog)
    dp.include_router(manage_guides_dialog)
    dp.include_router(add_guide_dialog)
    dp.include_router(guides_dialog)
    dp.include_router(admin_feedback_dialog)
    dp.include_router(user_feedback_dialog)
