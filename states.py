from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()


class MenuSG(StatesGroup):
    menu = State()
    auth = State()
    company_info = State()
    org_structure = State()
    events = State()
    guides = State()
    virtexs = State()
    canteen = State()
    feedback = State()
    faq = State()


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


class LogoutSG(StatesGroup):
    """Класс состояния для logout"""

    logout = State()


class RegisterDialogSG(StatesGroup):
    """
    Состояния диалога регистрации нового пользователя.
    """

    first = State()
    last = State()
    middle = State()
    confirm = State()


class CompanyInfoCreationSG(StatesGroup):
    """
    Состояния для диалога создания новой информации о компании.
    """

    title = State()
    description = State()
    file = State()
    image = State()
    confirm = State()


class ManageCompanyInfoSG(StatesGroup):
    """
    Состояния для диалога редактирования информации о компании.
    """
    list = State()
    company_info_action = State()
    edit_title = State()
    edit_description = State()
    edit_file = State()
    edit_image = State()


class CompanyInfoViewSG(StatesGroup):
    """
    Состояния для просмотра информации о компании
    """

    list = State()
    detail = State()


class OrgStructureCreationSG(StatesGroup):
    """
    Состояния для диалога создания новой организационной структуры.
    """

    title = State()
    description = State()
    file = State()
    confirm = State()


class ManageOrgStructureSG(StatesGroup):
    """
    Состояния для управления организационной структурой.
    """
    list = State()
    org_structure_action = State()
    edit_title = State()
    edit_description = State()
    edit_file = State()


class OrgStructureViewSG(StatesGroup):
    """
    Состояния для просмотра организационной структуры.
    """

    list = State()
    detail = State()


class EventCreationSG(StatesGroup):
    """
    Состояния диалога добавления мероприятий.
    """
    title = State()
    description = State()
    confirm = State()


class ManageEventSG(StatesGroup):
    """
    Состояния диалога управления мероприятиями.
    """
    list = State()
    event_action = State()
    edit_title = State()
    edit_description = State()


class EventsViewSG(StatesGroup):
    """
    Состояния диалога просмотра мероприятий.
    """

    list = State()
    detail = State()


class GuideCreationSG(StatesGroup):
    """
    Состояния диалога создания инструкций.
    """
    document = State()
    title = State()
    upload_content = State()
    end = State()


class GuideViewSG(StatesGroup):
    """
    Состояния диалога просмотра инструкций.
    """
    documents = State()
    guides = State()
    guide = State()
    end = State()


class GuideEditSG(StatesGroup):
    """
    Состояния диалога редактирования инструкций.
    """
    documents = State()
    guides = State()
    guide = State()
    edit_title = State()
    edit_doc_name = State()
    edit_content = State()
    delete_doc = State()
    delete_guide = State()
    end = State()


class ExcursionCreationSG(StatesGroup):
    """
    Состояния диалога создания виртуальных экскурсий.
    """
    title = State()
    description = State()
    confirm = State()
    material_name = State()
    upload_materials = State()
    material_end = State()


class ExcursionViewSG(StatesGroup):
    """
    Состояния диалога просмотра виртуальных экскурсий.
    """
    list = State()
    detail = State()
    material = State()


class ExcursionEditSG(StatesGroup):
    """
    Состояния диалога редактирования виртуальных экскурсий.
    """
    list = State()
    detail = State()
    material = State()
    edit_title = State()
    edit_description = State()
    edit_material_name = State()
    edit_material = State()
    delete_virtex = State()
    delete_material = State()


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


class FeedbackUserSG(StatesGroup):
    """
    Состояния для диалога добавления отзыва
    """
    text = State()
    attachment = State()
    end = State()


class FeedbackAdminSG(StatesGroup):
    """
    Состояния для диалога просмотра отзывов
    """
    list = State()
    detail = State()
    attachment = State()
    delete = State()


class AddFAQSG(StatesGroup):
    """
    Состояния для диалога добавления FAQ
    """

    method = State()
    question = State()
    answer = State()
    category = State()
    keywords = State()
    confirm = State()
    upload_excel = State()


class ManageFAQSQ(StatesGroup):
    """Состояния для управления FAQ"""

    list = State()
    faq_action = State()
    edit_question = State()
    edit_answer = State()
    edit_category = State()
    edit_keywords = State()


class FAQSearchSG(StatesGroup):
    """
    Состояния для диалога поиска FAQ
    """

    search_input = State()
    search_results = State()
    detail = State()


class FAQViewSG(StatesGroup):
    """
    Состояния для диалога FAQ
    """

    menu = State()
    list_all = State()
    category_select = State()
    category_questions = State()
    detail = State()
