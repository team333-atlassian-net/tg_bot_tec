from sqlalchemy import insert, select
from models import OrganizationalStructure
from db import async_session_maker

async def add_organizational_structure(title: str,
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



async def get_all_organizational_structure():
    async with async_session_maker() as session:
        result = await session.execute(select(OrganizationalStructure))
        return result.scalars().all()