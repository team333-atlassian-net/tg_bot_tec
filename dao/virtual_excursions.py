# dao.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import VirtualExcursion, ExcursionMaterial
from db import async_session_maker

# ---- Виртуальные экскурсии ----


async def create_virtex(title: str, description: str = None) -> VirtualExcursion:
    async with async_session_maker() as session:
        virtex = VirtualExcursion(title=title, description=description)
        session.add(virtex)
        await session.commit()
        await session.refresh(virtex)
        return virtex


async def get_virtex_by_id(virtex_id: int) -> VirtualExcursion | None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(VirtualExcursion).where(VirtualExcursion.id == virtex_id)
        )
        return result.scalar_one_or_none()


async def get_virtex_by_name(virtex_title: str) -> VirtualExcursion | None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(VirtualExcursion).where(VirtualExcursion.title == virtex_title)
        )
        return result.scalar_one_or_none()


async def get_all_virtexs() -> list[VirtualExcursion]:
    async with async_session_maker() as session:
        result = await session.execute(select(VirtualExcursion))
        return result.scalars().all()


async def update_virtex_title(virtex_id: int, new_title: str):
    async with async_session_maker() as session:
        virtex = await session.get(VirtualExcursion, virtex_id)
        if virtex:
            virtex.title = new_title
            await session.commit()


async def update_virtex_description(virtex_id: int, new_description: str):
    async with async_session_maker() as session:
        virtex = await session.get(VirtualExcursion, virtex_id)
        if virtex:
            virtex.description = new_description
            await session.commit()


async def delete_virtex(virtex_id: int):
    async with async_session_maker() as session:
        virtex = await session.get(VirtualExcursion, virtex_id)
        if virtex:
            await session.delete(virtex)
            await session.commit()


# ---- Материалы ----


async def add_material(
    virtex_id: int,
    telegram_file_id: str = None,
    name: str = None,
    text: str = None,
) -> ExcursionMaterial:
    async with async_session_maker() as session:
        material = ExcursionMaterial(
            excursion_id=virtex_id,
            telegram_file_id=telegram_file_id,
            name=name,
            text=text,
        )
        session.add(material)
        await session.commit()
        return material


async def get_materials_for_virtex(virtex_id: int) -> list[ExcursionMaterial]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(ExcursionMaterial).where(ExcursionMaterial.excursion_id == virtex_id)
        )
        return result.scalars().all()


async def get_material_by_id(material_id: int) -> ExcursionMaterial | None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(ExcursionMaterial).where(ExcursionMaterial.id == material_id)
        )
        return result.scalar_one_or_none()


async def update_material_name(material_id: int, new_name: str):
    async with async_session_maker() as session:
        material = await session.get(ExcursionMaterial, material_id)
        if material:
            material.name = new_name
            await session.commit()


async def update_material(
    material_id: int, new_telegram_file_id: int = None, new_text: str = None
):
    async with async_session_maker() as session:
        material = await session.get(ExcursionMaterial, material_id)
        if material:
            if new_telegram_file_id:
                material.telegram_file_id = new_telegram_file_id
            if new_text:
                material.text = new_text
            await session.commit()


async def delete_material(material_id: int):
    async with async_session_maker() as session:
        material = await session.get(ExcursionMaterial, material_id)
        if material:
            await session.delete(material)
            await session.commit()
