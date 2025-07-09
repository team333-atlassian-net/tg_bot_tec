from sqlalchemy import insert, select
from models import CompanyInfo
from db import async_session_maker

async def add_company_info(title: str,
                           content: str,
                           file_path: str = None,
                           image_path: str = None):
    async with async_session_maker() as session:
        stmt = insert(CompanyInfo).values(
            title=title,
            content=content,
            file_path=file_path,
            image_path=image_path,
        )
        await session.execute(stmt)
        await session.commit()



async def get_all_company_info():
    async with async_session_maker() as session:
        result = await session.execute(select(CompanyInfo))
        return result.scalars().all()