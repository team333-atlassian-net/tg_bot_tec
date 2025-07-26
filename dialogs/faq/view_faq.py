import logging

from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Row, Radio, ScrollingGroup

from dao.faq import get_all_faq, get_faq_by_id, get_all_categories, get_faq_by_category

logger = logging.getLogger(__name__)

class FAQSG(StatesGroup):
    """
    Состояния для диалога FAQ
    """
    menu = State()
    list_all = State()
    category_select = State()
    category_questions = State()
    detail = State()

# --- Геттеры ---

async def detail_window_getter(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для окна с подробной информацией о вопросе.
    Используется для передачи данных в шаблон Format.
    """
    data = await get_faq_detail(dialog_manager)
    return data


async def get_faq_list(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает список всех вопросов FAQ.
    """
    faqs = await get_all_faq()
    return {"faqs": [(str(f.id), f.question) for f in faqs]}


async def get_category_list(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает список всех доступных категорий FAQ.
    """
    categories = await get_all_categories()
    return {"categories": categories}


async def get_faqs_by_category(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает вопросы FAQ, отфильтрованные по выбранной категории.
    """
    category = dialog_manager.dialog_data.get("selected_category")
    if not category:
        return {
            "category": "❌ Категория не выбрана",
            "faqs": []
        }

    faqs = await get_faq_by_category(category)
    return {
        "category": category,
        "faqs": [(str(f.id), f.question) for f in faqs]
    }


async def get_faq_detail(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает подробную информацию о выбранном вопросе.
    """
    faq_id = int(dialog_manager.dialog_data["selected_faq_id"])
    faq = await get_faq_by_id(faq_id)
    return {"faq": faq}

# --- Коллбэки ---

async def on_faq_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_id: str):
    """
    Обрабатывает выбор вопроса из списка. Переходит на окно с деталями.
    """
    manager.dialog_data["selected_faq_id"] = int(selected_id)
    manager.dialog_data["from_state"] = manager.current_context().state.state
    await manager.switch_to(FAQSG.detail)


async def on_category_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_id: str):
    """
    Обрабатывает выбор категории. Сохраняет выбранную категорию и переходит к списку вопросов по ней.
    """
    manager.dialog_data["selected_category"] = selected_id
    await manager.switch_to(FAQSG.category_questions)


async def on_detail_back(callback: CallbackQuery, button: Button, manager: DialogManager):
    """
    Возвращает на окно, с которого пользователь попал на детали вопроса.
    """
    from_state = manager.dialog_data.get("from_state")
    manager.dialog_data.pop("from_state", None)

    if from_state == FAQSG.list_all.state:
        await manager.switch_to(FAQSG.list_all)
    elif from_state == FAQSG.category_questions.state:
        await manager.switch_to(FAQSG.category_questions)
    else:
        await manager.switch_to(FAQSG.menu)


async def on_back_to_menu(callback: CallbackQuery, button: Button, manager: DialogManager):
    """
    Обрабатывает кнопку "Назад" к главному меню из категорий.
    """
    await manager.switch_to(FAQSG.menu)

# --- ОКНА ---

# Главное меню
faq_menu_window = Window(
    Const("📚 Что вы хотите сделать?"),
    Button(
        Const("📋 Посмотреть все вопросы"),
        id="all",
        on_click=lambda c, b, m: m.switch_to(FAQSG.list_all),
    ),
    Button(
        Const("🏷 Посмотреть все категории вопросов"),
        id="by_cat",
        on_click=lambda c, b, m: m.switch_to(FAQSG.category_select),
    ),
    Cancel(Const("❌ Отмена")),
    state=FAQSG.menu,
)

# Список всех вопросов
faq_list_window = Window(
    Const("📋 Все вопросы:"),
    ScrollingGroup(
        Radio(
            Format("{item[1]}"),
            Format("{item[1]}"),
            id="faq_radio",
            items="faqs",
            item_id_getter=lambda x: x[0],
            on_click=on_faq_selected,
        ),
        id="faq_scroll",
        width=1,
        height=5,
    ),
    Back(Const("⬅️ Назад")),
    state=FAQSG.list_all,
    getter=get_faq_list,
)

# Список всех категорий
faq_category_select_window = Window(
    Const("📋 Выберите категорию:"),
    ScrollingGroup(
        Radio(
            Format("{item}"),
            Format("{item}"),
            id="cat_radio",
            items="categories",
            item_id_getter=lambda x: x,
            on_click=on_category_selected,
        ),
        id="cat_scroll",
        width=1,
        height=5,
    ),
    Button(Const("⬅️ Назад"), id="back_to_menu_from_cat", on_click=on_back_to_menu),
    state=FAQSG.category_select,
    getter=get_category_list,
)

# Список вопросов по категории
faq_by_category_window = Window(
    Format("📂 Вопросы по категории: <b>{category}</b>"),
    ScrollingGroup(
        Radio(
            Format("{item[1]}"),
            Format("{item[1]}"),
            id="faq_cat_radio",
            items="faqs",
            item_id_getter=lambda x: x[0],
            on_click=on_faq_selected,
        ),
        id="faq_cat_scroll",
        width=1,
        height=5,
    ),
    Back(Const("⬅️ Назад")),
    state=FAQSG.category_questions,
    getter=get_faqs_by_category,
)

# Детали вопроса
faq_detail_window = Window(
    Format("📌 <b>{faq.question}</b>\n\n{faq.answer}"),
    Row(
        Button(Const("⬅️ Назад"), id="back_from_detail", on_click=on_detail_back),
        Cancel(Const("❌ Закрыть")),
    ),
    state=FAQSG.detail,
    getter=detail_window_getter,
)

faq_dialog = Dialog(
    faq_menu_window,
    faq_list_window,
    faq_category_select_window,
    faq_by_category_window,
    faq_detail_window,
)
