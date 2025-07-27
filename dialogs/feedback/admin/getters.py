import logging
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram.enums import ContentType
from dao.feedback import *

logger = logging.getLogger(__name__)


async def feedbacks_getter(dialog_manager: DialogManager, **kwargs):
    if dialog_manager.start_data["unread_flag"]:
        feedbacks = await get_feedbacks(is_read=False)
        unread = True
    else:
        feedbacks = await get_feedbacks()
        unread = False
    res = {
        "feedbacks": [(f.id, f) for f in feedbacks],
        "unread": unread,
        "all": not unread,
    }
    return res


async def feedback_detail_getter(dialog_manager: DialogManager, **kwargs):
    feedback_id = dialog_manager.dialog_data["feedback_id"]
    feedback = await get_feedback_by_id(feedback_id=feedback_id)
    attachments = await get_attachments_by_feedback_id(feedback_id=feedback_id)
    return {
        "feedback": feedback,
        "attachments": [
            (attachments[i].id, "Вложение " + str(i + 1))
            for i in range(len(attachments))
        ],
    }


async def attachment_getter(dialog_manager: DialogManager, **kwargs):
    attachment_id = dialog_manager.dialog_data["attachment_id"]
    attachment = await get_attachment_by_id(attachment_id)
    file = MediaAttachment(ContentType.PHOTO, attachment.file_id)
    logger.info(file)
    return {"file": file}
