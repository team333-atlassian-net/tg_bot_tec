import logging

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from states import EventsViewSG

logger = logging.getLogger(__name__)


async def on_event_selected(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    """
    Обработчик выбора мероприятия из списка.
    Сохраняет выбранный event_id в dialog_data и переключает состояние на detail.

    Args:
        selected_id (str): ID выбранного мероприятия.
    """
    manager.dialog_data["selected_event_id"] = int(selected_id)
    await manager.switch_to(EventsViewSG.detail)
