from sqlalchemy import insert, select
from models import OrganizationalStructure
from db import async_session_maker

async def add_org_structure(title: str,
                           content: str,
                           file_id: str = None):
    async with async_session_maker() as session:
        stmt = insert(OrganizationalStructure).values(
            title=title,
            content=content,
            file_id=file_id,
        )
        await session.execute(stmt)
        await session.commit()


async def get_all_org_structures():
    async with async_session_maker() as session:
        result = await session.execute(select(OrganizationalStructure))
        return result.scalars().all()


async def get_org_structure_by_id(org_structure_id: int):
    async with async_session_maker() as session:
        res = await session.execute(select(OrganizationalStructure).where(OrganizationalStructure.id == org_structure_id))
        return res.scalar_one_or_none()


async def update_org_structure(org_structure_id: int, new_title: str = None, new_description: str = None, file_id: str = None):
    async with async_session_maker() as session:
        org_structure = await session.get(OrganizationalStructure, org_structure_id)
        if org_structure:
            if new_title is not None:
                org_structure.title = new_title
            if new_description is not None:
                org_structure.description = new_description
            if file_id is not None:
                org_structure.file_id = file_id
            await session.commit()

async def delete_org_structure(org_structure_id: str):
    async with async_session_maker() as session:
        org_structure = await session.get(OrganizationalStructure, org_structure_id)
        if org_structure:
            await session.delete(org_structure)
            await session.commit()
