import logging
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput, TextInput
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.kbd import (
    Back,
    Next,
    Cancel,
    Row,
    Button,
    SwitchTo,
    Group,
    Select,
    ScrollingGroup,
)
from aiogram_dialog.widgets.text import Const, Format
from aiogram.enums import ContentType
from aiogram.enums import ContentType
from states import FeedbackAdminSG
from dao.feedback import *
from dialogs.feedback.admin.handlers import *
from dialogs.feedback.admin.getters import *

logger = logging.getLogger(__name__)


feedback_list_window = Window(
    Const("<b>Непрочитанные отзывы</b>\n\n", when="unread"),
    Const("<b>Все отзывы</b>\n\n", when="all"),
    Const("Выберите отзыв для подробного просмотра"),
    ScrollingGroup(
        Select(
            Format("{item[1].text:.15}..."),
            id="feedback_select",
            item_id_getter=lambda item: item[0],
            items="feedbacks",
            on_click=on_feedback_select,
        ),
        id="scroll_feedbacks",
        width=1,
        height=5,
    ),
    Button(
        Const("Показать все отзывы"),
        id="show_all_btn",
        on_click=on_show_all_press,
        when="unread",
    ),
    Button(
        Const("Показать непрочитанные отзывы"),
        id="show_unread_btn",
        on_click=on_show_unread_press,
        when="all",
    ),
    Cancel(Const("❌ Отмена")),
    state=FeedbackAdminSG.feedback_list,
    getter=feedbacks_getter,
)

feedback_detail_window = Window(
    Format("📌 Отзыв:\n\n{feedback.text}"),
    ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id="attachment_select",
            item_id_getter=lambda item: item[0],
            items="attachments",
            on_click=on_attachment_select,
        ),
        id="scroll_attachments",
        width=3,
        height=1,
    ),
    Group(
        Button(
            Const("Отметить прочитанным"),
            id="set_read_btn",
            on_click=on_set_read,
        ),
        Button(
            Const("Удалить отзыв"),
            id="delete_feedback_btn",
            on_click=on_press_delete_feedback,
        ),
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Закрыть")),
    ),
    state=FeedbackAdminSG.feedback_detail,
    getter=feedback_detail_getter,
)

attachment_window = Window(
    DynamicMedia("file"),
    Row(Back(Const("⬅️ Вернуться к отзыву")), Cancel(Const("❌ Закрыть"))),
    state=FeedbackAdminSG.attachment,
    getter=attachment_getter,
)


delete_feedback_window = Window(
    Const("Вы уверены, что хотите удалить отзыв?"),
    Cancel(Const("❌ Отмена")),
    Button(
        Const("Да, удалить"),
        on_click=on_delete_feedback,
        id="confirm_delete_feedback_btn",
    ),
    state=FeedbackAdminSG.delete,
)


dialog = Dialog(
    feedback_list_window,
    feedback_detail_window,
    attachment_window,
    delete_feedback_window,
)
