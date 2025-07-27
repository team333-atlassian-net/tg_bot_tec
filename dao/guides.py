from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from models import Guide
from db import async_session_maker


async def create_guide(
    document: str, title: str, text: str = None, file_id: str = None
) -> Guide:
    async with async_session_maker() as session:
        guide = Guide(document=document, title=title, text=text, file_id=file_id)
        session.add(guide)
        await session.commit()
        await session.refresh(guide)
        return guide


async def get_guide_by_id(guide_id: int) -> Guide | None:
    async with async_session_maker() as session:
        result = await session.execute(select(Guide).where(Guide.id == guide_id))
        return result.scalar_one_or_none()


async def get_all_documents() -> list[str] | None:
    async with async_session_maker() as session:
        result = await session.execute(select(Guide.document).distinct())
        return result.scalars().all()


async def get_guides_by_document(document: str) -> list[Guide]:
    async with async_session_maker() as session:
        result = await session.execute(select(Guide).where(Guide.document == document))
        return result.scalars().all()


async def update_doc_name(old_doc_name: str, new_doc_name: str):
    async with async_session_maker() as session:
        stmt = (
            update(Guide)
            .where(Guide.document == old_doc_name)
            .values(document=new_doc_name)
        )
        await session.execute(stmt)
        await session.commit()


async def update_guide_title(guide_id: int, new_title: str):
    async with async_session_maker() as session:
        guide = await session.get(Guide, guide_id)
        if guide:
            guide.title = new_title
            await session.commit()


async def update_guide_content(
    guide_id: int, new_file_id: str = None, new_text: str = None
):
    async with async_session_maker() as session:
        guide = await session.get(Guide, guide_id)
        if guide:
            if new_file_id:
                guide.file_id = new_file_id
            if new_text:
                guide.text = new_text
            await session.commit()


async def delete_guide(guide_id: int):
    async with async_session_maker() as session:
        guide = await session.get(Guide, guide_id)
        if guide:
            await session.delete(guide)
            await session.commit()


async def delete_all_guide_by_document(document: str):
    async with async_session_maker() as session:
        stmt = delete(Guide).where(Guide.document == document)
        await session.execute(stmt)
        await session.commit()
