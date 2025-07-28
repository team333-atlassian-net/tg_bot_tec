from aiogram_dialog import Window, Dialog, StartMode, LaunchMode
from aiogram_dialog.widgets.kbd import Start, Next, Select, Button, Group, Back, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from dialogs.auth.logout.handlers import on_logout
from dialogs.menu.getters import *
from dialogs.menu.handlers import *
from states import *

menu_window = Window(
    Format("{not_auth_text}", when="is_not_auth"),
    Start(Const("Войти по пин-коду"),
          id="start_auth",
          state=AuthDialogSG.enter_pin,
          when="is_not_auth",
          mode=StartMode.NORMAL),
    Start(Const("Зарегистрироваться"),
          id="start_register",
          state=RegisterDialogSG.first,
          when="is_not_auth",
          mode=StartMode.NORMAL),
    Format("{auth_text}", when="is_auth"),
    Group(
        Button(Const("Авторизация"),
               id="to_auth_module_btn",
               on_click=on_auth_click),
        Button(Const("Информация о компании"),
               id="to_info_module_btn",
               on_click=on_info_click),
        Button(Const("Столовая"),
               id="to_canteen_btn",
               on_click=on_canteen_click),
        Button(Const("Экскурсии"),
               id="to_excursion_btn",
               on_click=on_excursion_click),
        Button(Const("Гайды"),
               id="to_guides_btn",
               on_click=on_guide_click),
        Button(Const("Отзывы"),
               id="to_feedback_btn",
               on_click=on_feedback_click),
        Button(Const("Мероприятия"),
               id="to_events_btn",
               on_click=on_events_click),
        Button(Const("Орг. структура"),
               id="to_org_structure_btn",
               on_click=on_org_structure_click),
        Button(Const("FAQ"),
               id="to_faq_btn",
               on_click=on_faq_click),
        when="is_auth"
    ),
    getter=auth_getter,
    state=MenuSG.menu
)

# Auth / Регистрация / Добавление пользователя
auth_module_window = Window(
    Const("Выберите действие:"),
    Start(Const("Авторизация"),
          id="start_auth_dialog",
          state=AuthDialogSG.enter_pin,
          mode=StartMode.NORMAL),
    Start(Const("Регистрация"),
          id="start_register_dialog",
          state=RegisterDialogSG.first,
          mode=StartMode.NORMAL),
    Button(Const("Выход"), id="start_logout", on_click=on_logout),
    Start(Const("Добавить пользователя(ей)"),
          id="start_add_user",
          state=AddUserSG.method,
          mode=StartMode.NORMAL,
          when="is_admin"),
    SwitchTo(Const("⬅️ Назад"), state=MenuSG.menu, id="from_auth_to_menu"),
    state=MenuSG.auth,
    getter=role_getter
)

# Информация о компании
company_info_module_window = Window(
    Const("Выберите действие:"),
    Start(Const("Добавить информацию о компании"),
          id="start_company_info_create",
          state=CompanyInfoCreationSG.title,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Управлять информацией о компании"),
          id="start_manage_company_info",
          state=ManageCompanyInfoSG.list,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Посмотреть информацию о компании"),
          id="start_view_company_info",
          state=CompanyInfoViewSG.list,
          mode=StartMode.NORMAL),
    SwitchTo(Const("⬅️ Назад"), state=MenuSG.menu, id="from_info_to_menu"),
    state=MenuSG.company_info,
    getter=role_getter
)

# Организационная структура
org_structure_module_window = Window(
    Const("Выберите действие:"),
    Start(Const("Добавить орг. структуру"),
          id="start_create_org_structure",
          state=OrgStructureCreationSG.title,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Управлять орг. структурой"),
          id="start_manage_org_structure",
          state=ManageOrgStructureSG.list,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Посмотреть орг. структуру"),
          id="start_view_org_structure",
          state=OrgStructureViewSG.list,
          mode=StartMode.NORMAL),
    SwitchTo(Const("⬅️ Назад"), state=MenuSG.menu, id="from_org_structure_to_menu"),
    state=MenuSG.org_structure,
    getter=role_getter
)

# Мероприятия
events_module_window = Window(
    Const("Выберите действие:"),
    Start(Const("Добавить мероприятие"),
          id="start_create_event",
          state=EventCreationSG.title,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Управлять мероприятиями"),
          id="start_manage_events",
          state=ManageEventSG.list,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Посмотреть мероприятия"),
          id="start_view_events",
          state=EventsViewSG.list,
          mode=StartMode.NORMAL),
    SwitchTo(Const("⬅️ Назад"), state=MenuSG.menu, id="from_events_to_menu"),
    state=MenuSG.events,
    getter=role_getter
)

# Гайды
guide_module_window = Window(
    Const("Выберите действие:"),
    Start(Const("Добавить инструкцию"),
          id="start_create_guide",
          state=GuideCreationSG.document,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Редактировать инструкции"),
          id="start_edit_guide",
          state=GuideEditSG.documents,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Посмотреть инструкции по оформлению документов"),
          id="start_view_guide",
          state=GuideViewSG.documents,
          mode=StartMode.NORMAL),
    SwitchTo(Const("⬅️ Назад"), state=MenuSG.menu, id="from_guides_to_menu"),
    state=MenuSG.guides,
    getter=role_getter
)

# Экскурсии
virtexs_module_window = Window(
    Const("Выберите действие:"),
    Start(Const("Создать виртуальную экскурсию"),
          id="start_create_excursion",
          state=ExcursionCreationSG.title,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Редактировать виртуальные экскурсии"),
          id="start_edit_excursion",
          state=ExcursionEditSG.list,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Посмотреть виртуальные экскурсии"),
          id="start_view_excursion",
          state=ExcursionViewSG.list,
          mode=StartMode.NORMAL),
    SwitchTo(Const("⬅️ Назад"), state=MenuSG.menu, id="from_virtexs_to_menu"),
    state=MenuSG.virtexs,
    getter=role_getter
)
# Столовая
canteen_module_window = Window(
    Const("Выберите действие:"),
    Start(Const("Добавить информацию о столовой/меню"),
          id="start_canteen_create",
          state=CanteenInfoCreationSG.choice,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Управление информацией о столовой/меню"),
          id="start_manage_canteen",
          state=ManageCanteenSG.choice,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Посмотреть информацию о столовой/меню"),
          id="start_view_canteen",
          state=CanteenViewSG.start,
          mode=StartMode.NORMAL),
    SwitchTo(Const("⬅️ Назад"), state=MenuSG.menu, id="from_canteen_to_menu"),
    state=MenuSG.canteen,
    getter=role_getter
)

# Обратная связь
feedback_module_window = Window(
    Const("Выберите действие:"),
    Start(Const("Оставить отзыв"),
          id="start_feedback_user",
          state=FeedbackUserSG.text,
          mode=StartMode.NORMAL),
    Start(Const("Посмотреть отзывы"),
          id="start_feedback_admin",
          state=FeedbackAdminSG.list,
          mode=StartMode.NORMAL,
          when="is_admin",
          data={"unread_flag": True}),
    SwitchTo(Const("⬅️ Назад"), state=MenuSG.menu, id="from_feedback_to_menu"),
    state=MenuSG.feedback,
    getter=role_getter
)

# FAQ
faq_module_window = Window(
    Const("Выберите действие:"),
    Start(Const("Добавить FAQ"),
          id="start_add_faq",
          state=AddFAQSG.method,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Управлять FAQ"),
          id="start_manage_faq",
          state=ManageFAQSQ.list,
          mode=StartMode.NORMAL,
          when="is_admin"),
    Start(Const("Поиск FAQ"),
          id="start_search_faq",
          state=FAQSearchSG.search_input,
          mode=StartMode.NORMAL),
    Start(Const("Посмотреть FAQ"),
          id="start_view_faq",
          state=FAQViewSG.menu,
          mode=StartMode.NORMAL),
    SwitchTo(Const("⬅️ Назад"), state=MenuSG.menu, id="from_faq_to_menu"),
    state=MenuSG.faq,
    getter=role_getter
)

dialog = Dialog(menu_window,
                auth_module_window,
                company_info_module_window,
                org_structure_module_window,
                events_module_window,
                guide_module_window,
                virtexs_module_window,
                canteen_module_window,
                feedback_module_window,
                faq_module_window, launch_mode=LaunchMode.ROOT)
