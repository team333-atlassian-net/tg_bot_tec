import logging
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram.enums import ContentType
from dao.guides import *


async def documents_getter(dialog_manager: DialogManager, **kwargs):
    docs = await get_all_documents()
    return {"docs": [(i, docs[i]) for i in len(docs)]}
