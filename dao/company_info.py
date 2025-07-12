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
    

async def get_company_info_by_id(company_info_id: int):
    async with async_session_maker() as session:
        res = await session.execute(select(CompanyInfo).where(CompanyInfo.id == company_info_id))
        return res.scalar_one_or_none()


async def update_company_info(company_info_id: int,
                               new_title: str = None,
                               new_description: str = None,
                               file_id: str = None,
                               image_id: str = None):
    async with async_session_maker() as session:
        company_info = await session.get(CompanyInfo, company_info_id)
        if company_info:
            if new_title is not None:
                company_info.title = new_title
            if new_description is not None:
                company_info.content = new_description
            if file_id is not None:
                company_info.file_path = file_id
            if image_id is not None:
                company_info.image_path = image_id
            await session.commit()

async def delete_company_info(company_info_id: str):
    async with async_session_maker() as session:
        company_info = await session.get(CompanyInfo, company_info_id)
        if company_info:
            await session.delete(company_info)
            await session.commit()
