import logging
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram.enums import ContentType
from dao.virtual_excursions import *


async def get_excursion_list(dialog_manager: DialogManager, **kwargs):
    excursions = await get_all_virtexs()
    return {"virtexs": [(str(e.id), e.title) for e in excursions]}


async def get_excursion_detail(dialog_manager: DialogManager, **kwargs):
    excursion_id = int(dialog_manager.dialog_data["selected_virtex_id"])
    excursion = await get_virtex_by_id(excursion_id)
    materials = await get_materials_for_virtex(excursion_id)

    return {
        "virtex": excursion,
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
