import logging

from aiogram_dialog import DialogManager

from dao.faq import get_all_faq, get_faq_by_id, get_all_categories, get_faq_by_category

logger = logging.getLogger(__name__)


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
        return {"category": "❌ Категория не выбрана", "faqs": []}

    faqs = await get_faq_by_category(category)
    return {"category": category, "faqs": [(str(f.id), f.question) for f in faqs]}


async def get_faq_detail(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает подробную информацию о выбранном вопросе.
    """
    faq_id = int(dialog_manager.dialog_data["selected_faq_id"])
    faq = await get_faq_by_id(faq_id)
    return {"faq": faq}
