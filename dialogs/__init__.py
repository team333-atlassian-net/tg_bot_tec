from aiogram_dialog import setup_dialogs
from aiogram import Dispatcher

from dialogs.start.dialog import dialog as start_dialog
from dialogs.menu.dialog import dialog as menu_dialog

from dialogs.auth.login.dialog import dialog as login_dialog
from dialogs.auth.register.dialog import dialog as register_dialog
from dialogs.auth.add_user.dialog import dialog as add_user_dialog
from dialogs.auth.logout.dialog import dialog as logout_dialog

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


def get_dialogs():
    return [
        start_dialog,
        menu_dialog,
        login_dialog,
        logout_dialog,
        register_dialog,
        add_user_dialog,
        view_event_dialog,
        manage_event_dialog,
        create_event_dialog,
        create_org_structure_dialog,
        manage_org_structure_dialog,
        org_structure_dialog,
        create_company_info_dialog,
        create_virtex_dialog,
        virtex_dialog,
        edit_virtex_dialog,
        company_info_dialog,
        manage_company_info_dialog,
        add_faq_dialog,
        faq_dialog,
        faq_search_dialog,
        manage_faq_dialog,
        add_canteen_info_dialog,
        canteen_dialog,
        manage_canteen_dialog,
        manage_guides_dialog,
        add_guide_dialog,
        guides_dialog,
        admin_feedback_dialog,
        user_feedback_dialog,
    ]
