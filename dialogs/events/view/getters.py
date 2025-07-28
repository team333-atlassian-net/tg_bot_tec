import logging

from aiogram_dialog import DialogManager

from dao.events import get_all_events, get_event_by_id

logger = logging.getLogger(__name__)


async def get_event_list(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для получения списка мероприятий.
    Возвращает список кортежей (id, title) мероприятий,
    который используется для отображения в Select или Radio.

    Returns:
        dict: {'events': [(id, title), ...]}
    """
    events = await get_all_events()
    return {"events": [(str(e.id), e.title) for e in events]}


async def get_event_detail(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для получения подробной информации о выбранном мероприятии.
    Использует сохранённый event_id из dialog_data.

    Returns:
        dict: {'event': Event}
    """
    event_id = int(dialog_manager.dialog_data["selected_event_id"])
    event = await get_event_by_id(event_id)
    return {"event": event}


async def detail_window_getter(dialog_manager: DialogManager, **kwargs):
    """
    Геттер для окна с подробной информацией о мероприятии.
    Используется для передачи данных в шаблон Format.

    Returns:
        dict: {'event': Event}
    """
    data = await get_event_detail(dialog_manager)
    return data
