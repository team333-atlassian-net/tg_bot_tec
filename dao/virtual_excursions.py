# dao.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import VirtualExcursion, ExcursionMaterial
from db import async_session_maker

# ---- Виртуальные экскурсии ----


async def create_excursion(title: str, description: str = None) -> VirtualExcursion:
    async with async_session_maker() as session:
        excursion = VirtualExcursion(title=title, description=description)
        session.add(excursion)
        await session.commit()
        await session.refresh(excursion)
        return excursion


async def get_excursion_by_id(excursion_id: int) -> VirtualExcursion | None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(VirtualExcursion).where(VirtualExcursion.id == excursion_id)
        )
        return result.scalar_one_or_none()


async def get_excursion_by_name(excursion_title: str) -> VirtualExcursion | None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(VirtualExcursion).where(VirtualExcursion.title == excursion_title)
        )
        return result.scalar_one_or_none()


async def get_all_excursions() -> list[VirtualExcursion]:
    async with async_session_maker() as session:
        result = await session.execute(select(VirtualExcursion))
        return result.scalars().all()


async def update_excursion(excursion_id: int, new_title: str, new_description):
    async with async_session_maker() as session:
        excursion = await session.get(VirtualExcursion, excursion_id)
        if excursion:
            excursion.title = new_title
            excursion.description = new_description
            await session.commit


async def delete_excursion(excursion_id: int):
    async with async_session_maker() as session:
        excursion = await session.get(VirtualExcursion, excursion_id)
        if excursion:
            await session.delete(excursion)
            await session.commit


# ---- Материалы ----


async def add_material(
    excursion_id: int,
    telegram_file_id: str = None,
    file_name: str = None,
    text: str = None,
) -> ExcursionMaterial:
    async with async_session_maker() as session:
        material = ExcursionMaterial(
            excursion_id=excursion_id,
            telegram_file_id=telegram_file_id,
            file_name=file_name,
            text=text,
        )
        session.add(material)
        await session.commit()
        await session.refresh(material)
        return material


async def get_materials_for_excursion(excursion_id: int) -> list[ExcursionMaterial]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(ExcursionMaterial).where(
                ExcursionMaterial.excursion_id == excursion_id
            )
        )
        return result.scalars().all()


async def update_material(material_id: int, new_file_name: str, new_telegram_file_id):
    async with async_session_maker() as session:
        material = await session.get(ExcursionMaterial, material_id)
        if material:
            material.file_name = new_file_name
            material.telegram_file_id = new_telegram_file_id
            await session.commit


async def delete_material(material_id: int):
    async with async_session_maker() as session:
        material = await session.get(ExcursionMaterial, material_id)
        if material:
            await session.delete(material)
            await session.commit
