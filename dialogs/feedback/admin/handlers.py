import logging
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.api.protocols import DialogManager
from aiogram.types import Message
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Select,
)
from dao.feedback import *
from states import FeedbackAdminSG


async def on_feedback_select(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["feedback_id"] = int(selected_id)
    await manager.switch_to(FeedbackAdminSG.detail)


async def on_show_all_press(callback, widget: Select, manager: DialogManager):
    manager.start_data["unread_flag"] = False
    await manager.switch_to(FeedbackAdminSG.list)


async def on_show_unread_press(callback, widget: Select, manager: DialogManager):
    manager.start_data["unread_flag"] = True
    await manager.switch_to(FeedbackAdminSG.list)


async def on_attachment_select(
    callback, widget: Select, manager: DialogManager, selected_id: str
):
    manager.dialog_data["attachment_id"] = int(selected_id)
    await manager.switch_to(FeedbackAdminSG.attachment)


async def on_set_read(callback, button: Button, dialog: DialogManager):
    feedback_id = dialog.dialog_data["feedback_id"]
    await mark_feedback_as_read(feedback_id=feedback_id)
    await dialog.switch_to(FeedbackAdminSG.list)


async def on_press_delete_feedback(callback, button: Button, dialog: DialogManager):
    await dialog.switch_to(FeedbackAdminSG.delete)


async def on_delete_feedback(callback, button: Button, dialog: DialogManager):
    feedback_id = dialog.dialog_data["feedback_id"]
    await delete_feedback(feedback_id=feedback_id)
    await dialog.switch_to(FeedbackAdminSG.list)
