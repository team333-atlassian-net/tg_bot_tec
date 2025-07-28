import logging

from aiogram_dialog import DialogManager

from dao.events import get_all_events, get_event_by_id

logger = logging.getLogger(__name__)


async def get_event_list(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает список всех мероприятий.
    """
    events = await get_all_events()
    return {"events": [(e.title, str(e.id)) for e in events]}


async def get_event_details(dialog_manager: DialogManager, **kwargs):
    """
    Возвращает детали выбранного мероприятия.
    """
    event_id = dialog_manager.dialog_data.get("event_id")
    if not event_id:
        return {"event_title": "Неизвестное мероприятие", "event_description": ""}
    event = await get_event_by_id(int(event_id))
    if not event:
        return {"event_title": "Мероприятие не найдено", "event_description": ""}
    return {
        "event_title": event.title,
        "event_description": event.description or "-",
    }
