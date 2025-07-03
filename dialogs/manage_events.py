from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format
from dao.events import delete_event, get_all_events, update_event

class ManageEventSG(StatesGroup):
    list = State()
    edit_title = State()
    edit_description = State()


async def get_event_list(dialog_manager: DialogManager, **kwargs):
    events = await get_all_events()
    return {
        "events": [(f"{e.title}", str(e.id)) for e in events]
    }

async def on_event_chosen(callback, widget, manager: DialogManager, item_id: str):
    manager.dialog_data["event_id"] = item_id
    await manager.switch_to(ManageEventSG.edit_title)

async def on_event_delete(callback, widget, manager: DialogManager, item_id: str):
    await delete_event(int(item_id))
    await callback.message.answer("✅ Мероприятие удалено.")
    await manager.switch_to(ManageEventSG.list)

async def on_edit_title(message: Message, value: str, dialog_manager: DialogManager, widget):
    dialog_manager.dialog_data["new_title"] = value.get_value()
    await dialog_manager.switch_to(ManageEventSG.edit_description)

async def on_edit_description(message: Message, value: str, dialog_manager: DialogManager, widget):
    new_description = value.get_value()
    new_title = dialog_manager.dialog_data["new_title"]
    event_id = dialog_manager.dialog_data["event_id"]
    await update_event(int(event_id), new_title, new_description)

    await message.answer("✏️ Мероприятие отредактировано.")
    await dialog_manager.switch_to(ManageEventSG.list)


manage_event_dialog = Dialog(
    Window(
        Const("📋 Список мероприятий:"),
        Select(Format("✏️ {item[0]}"), id="edit_event", item_id_getter=lambda x: x[1],
               items="events", on_click=on_event_chosen),
        Select(Format("🗑 Удалить: {item[0]}"), id="del_event", item_id_getter=lambda x: x[1],
               items="events", on_click=on_event_delete),
        state=ManageEventSG.list,
        getter=get_event_list,
    ),
    Window(
        Const("Введите новое название мероприятия:"),
        TextInput("edit_title", on_success=on_edit_title),
        state=ManageEventSG.edit_title,
    ),
    Window(
        Const("Введите новое описание:"),
        TextInput("edit_desc", on_success=on_edit_description),
        state=ManageEventSG.edit_description,
    ),
)