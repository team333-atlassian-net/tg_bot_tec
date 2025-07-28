from aiogram_dialog import setup_dialogs
from aiogram import Dispatcher

from dialogs.auth.login.dialog import dialog as login_dialog
from dialogs.auth.register.dialog import dialog as register_dialog
from dialogs.auth.add_user.dialog import dialog as add_user_dialog

from dialogs.virtual_excursions.create.dialog import dialog as create_virtex_dialog
from dialogs.virtual_excursions.view.dialog import dialog as virtex_dialog
from dialogs.virtual_excursions.edit.dialog import dialog as edit_virtex_dialog

from dialogs.events.view.dialog import dialog as view_event_dialog
from dialogs.events.edit.dialog import dialog as manage_event_dialog
from dialogs.events.create.dialog import dialog as create_event_dialog

from dialogs.org_structure.create.dialog import dialog as create_org_structure_dialog
from dialogs.org_structure.view.dialog import dialog as org_structure_dialog
from dialogs.org_structure.edit.dialog import dialog as manage_org_structure_dialog

from dialogs.company_info.create.dialog import dialog as create_company_info_dialog
from dialogs.company_info.view.dialog import dialog as company_info_dialog
from dialogs.company_info.edit.dialog import dialog as manage_company_info_dialog

from dialogs.faq.create.dialog import dialog as add_faq_dialog
from dialogs.faq.view.dialog import dialog as faq_dialog
from dialogs.faq.search.dialog import dialog as faq_search_dialog
from dialogs.faq.edit.dialog import dialog as manage_faq_dialog

from dialogs.canteen.create.dialog import dialog as add_canteen_info_dialog
from dialogs.canteen.view.dialog import dialog as canteen_dialog
from dialogs.canteen.edit.dialog import dialog as manage_canteen_dialog

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
