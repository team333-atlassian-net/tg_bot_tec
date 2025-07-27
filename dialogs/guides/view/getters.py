import logging
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram.enums import ContentType
from dao.guides import *

logger = logging.getLogger(__name__)


async def documents_getter(dialog_manager: DialogManager, **kwargs):
    docs = await get_all_documents()
    dialog_manager.dialog_data["docs"] = docs
    return {"docs": [(i, docs[i]) for i in range(len(docs))]}


async def guides_getter(dialog_manager: DialogManager, **kwargs):
    doc = dialog_manager.dialog_data["doc"]
    guides = await get_guides_by_document(doc)
    return {
        "doc": doc,
        "guides": [(guide.id, guide.title) for guide in guides],
    }


async def guide_getter(dialog_manager: DialogManager, **kwargs):
    guide = await get_guide_by_id(dialog_manager.dialog_data["guide_id"])
    file = (
        MediaAttachment(ContentType.DOCUMENT, guide.file_id) if guide.file_id else False
    )
    text = guide.text or False
    return {"file": file, "text": text}
