from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Format
from aiogram.fsm.state import State, StatesGroup
from dao.events import get_all_events

class ViewEventSG(StatesGroup):
    main = State()

async def get_events_data(dialog_manager: DialogManager, **kwargs):
    events = await get_all_events()
    if not events:
        return {"text": "Нет мероприятий"}
    text = "\n\n".join(f"🎉 <b>{e.title}</b>\n{e.description}" for e in events)
    return {"text": text}

view_event_dialog = Dialog(
    Window(
        Format("{text}"),
        state=ViewEventSG.main,
        getter=get_events_data,
    )
)