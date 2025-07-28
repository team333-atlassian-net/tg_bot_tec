import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from states import FAQViewSG


logger = logging.getLogger(__name__)


async def on_faq_selected(
    callback: CallbackQuery, widget, manager: DialogManager, selected_id: str
):
    """
    Обрабатывает выбор вопроса из списка. Переходит на окно с деталями.
    """
    manager.dialog_data["selected_faq_id"] = int(selected_id)
    manager.dialog_data["from_state"] = manager.current_context().state.state
    await manager.switch_to(FAQViewSG.detail)


async def on_category_selected(
    callback: CallbackQuery, widget, manager: DialogManager, selected_id: str
):
    """
    Обрабатывает выбор категории. Сохраняет выбранную категорию и переходит к списку вопросов по ней.
    """
    manager.dialog_data["selected_category"] = selected_id
    await manager.switch_to(FAQViewSG.category_questions)


async def on_detail_back(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    """
    Возвращает на окно, с которого пользователь попал на детали вопроса.
    """
    from_state = manager.dialog_data.get("from_state")
    manager.dialog_data.pop("from_state", None)

    if from_state == FAQViewSG.list_all.state:
        await manager.switch_to(FAQViewSG.list_all)
    elif from_state == FAQViewSG.category_questions.state:
        await manager.switch_to(FAQViewSG.category_questions)
    else:
        await manager.switch_to(FAQViewSG.menu)


async def on_back_to_menu(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    """
    Обрабатывает кнопку "Назад" к главному меню из категорий.
    """
    await manager.switch_to(FAQViewSG.menu)
