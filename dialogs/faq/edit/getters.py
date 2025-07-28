import logging

from aiogram_dialog import DialogManager
from dao.faq import get_all_faq, get_faq_by_id

logger = logging.getLogger(__name__)


async def get_faq_list(dialog_manager: DialogManager, **kwargs):
    """
    Получение списка всех вопросов для отображения в списке.
    Возвращает список кортежей (вопрос, id).
    """
    faq = await get_all_faq()
    return {"faq": [(f.question, str(f.id)) for f in faq]}


async def get_faq_details(dialog_manager: DialogManager, **kwargs):
    """
    Получение подробной информации по выбранному вопросу.
    Если вопрос не найден, возвращает значения по умолчанию.
    Форматирует ключевые слова в строку.
    """
    faq_id = dialog_manager.dialog_data.get("faq_id")
    if not faq_id:
        return {
            "faq_question": "Неизвестный вопрос",
            "faq_answer": "",
            "faq_category": "Не указана",
            "faq_keywords": "",
        }
    faq = await get_faq_by_id(int(faq_id))
    if not faq:
        return {
            "faq_question": "Вопрос не найден",
            "faq_answer": "",
            "faq_category": "Не указана",
            "faq_keywords": "",
        }
    keywords_str = ", ".join(kw.word for kw in faq.keywords) if faq.keywords else "-"
    return {
        "faq_question": faq.question,
        "faq_answer": faq.answer,
        "faq_category": faq.category or "-",
        "faq_keywords": keywords_str,
    }
