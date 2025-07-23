import logging
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram.enums import ContentType
from dao.virtual_excursions import *


async def get_virtex_list(dialog_manager: DialogManager, **kwargs):
    virtexs = await get_all_virtexs()
    return {"virtexs": [(str(e.id), e.title) for e in virtexs]}


async def get_virtex_detail(dialog_manager: DialogManager, **kwargs):
    virtex_id = int(dialog_manager.dialog_data["selected_virtex_id"])
    virtex = await get_virtex_by_id(virtex_id)
    materials = await get_materials_for_virtex(virtex_id)

    return {
        "virtex": virtex,
        "materials": [(material.id, material) for material in materials],
    }


async def material_getter(dialog_manager: DialogManager, **kwargs):
    material = await get_material_by_id(
        dialog_manager.dialog_data["selected_material_id"]
    )
    file = (
        MediaAttachment(ContentType.DOCUMENT, material.telegram_file_id)
        if material.telegram_file_id
        else False
    )
    text = material.text or False
    return {"file": file, "text": text}
