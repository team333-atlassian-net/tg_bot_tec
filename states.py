from aiogram.fsm.state import State, StatesGroup


class AddUserSG(StatesGroup):
    method = State()
    first_name = State()
    last_name = State()
    middle_name = State()
    confirm = State()
    upload_excel = State()


class AuthDialogSG(StatesGroup):
    """Класс состояния для авторизации"""

    enter_pin = State()


class RegisterDialogSG(StatesGroup):
    """
    Состояния диалога регистрации нового пользователя.
    """

    first = State()
    last = State()
    middle = State()
    confirm = State()


class CanteenInfoCreationSG(StatesGroup):
    """Состояния для диалога добавления информации о столовой и меню."""

    choice = State()

    # Состояния для столовой
    start_time = State()
    end_time = State()
    description = State()
    confirm_canteen = State()

    # Состояния для меню
    menu_date = State()
    menu_text = State()
    menu_file = State()
    confirm_menu = State()


class ManageCanteenSG(StatesGroup):
    """
    Состояния для управления меню и информацией о столовой.
    """

    choice = State()
    select_menu = State()
    menu_edit_action = State()
    edit_menu_text = State()
    edit_menu_file = State()
    confirm_menu_edit = State()
    confirm_info = State()

    edit_canteen_info = State()
    canteen_info_action = State()
    edit_info = State()
    edit_description = State()
    edit_start_time = State()
    edit_end_time = State()


class CanteenViewSG(StatesGroup):
    """Состояния диалога просмотра столовой и меню"""

    start = State()
    menu_list = State()
    menu_detail = State()
    calendar = State()
    info = State()


class ExcursionCreationSG(StatesGroup):
    title = State()
    description = State()
    confirm = State()
    material_name = State()
    upload_materials = State()
    material_end = State()


class ExcursionViewSG(StatesGroup):
    list = State()
    detail = State()
    material = State()


class ExcursionEditSG(StatesGroup):
    list = State()
    detail = State()
    material = State()
    edit_title = State()
    edit_description = State()
    edit_material_name = State()
    edit_material = State()
    delete_virtex = State()
    delete_material = State()


class GuideCreationSG(StatesGroup):
    document = State()
    title = State()
    upload_content = State()
    end = State()


class GuideViewSG(StatesGroup):
    documents = State()
    guides = State()
    guide = State()
    end = State()


class GuideEditSG(StatesGroup):
    documents = State()
    guides = State()
    guide = State()
    edit_title = State()
    edit_doc_name = State()
    edit_content = State()
    delete_doc = State()
    delete_guide = State()
    end = State()


class FeedbackUserSG(StatesGroup):
    text = State()
    attachment = State()
    end = State()


class FeedbackAdminSG(StatesGroup):
    feedback_list = State()
    feedback_detail = State()
    attachment = State()
    delete = State()
