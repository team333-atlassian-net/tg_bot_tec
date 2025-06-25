import pandas as pd
from models import FAQ
from sqlalchemy import or_, select
from db import async_session_maker

async def add_faq(faq):
    """Добавляет пользователя в БД"""
    async with async_session_maker() as session:
        session.add(faq)
        await session.commit()


async def search_faqs(query: str, category: str = None):
    async with async_session_maker() as session:
        stmt = select(FAQ).where(
            or_(
                FAQ.question.ilike(f"%{query}%"),
                FAQ.answer.ilike(f"%{query}%")
            )
        )
        if category:
            stmt = stmt.where(FAQ.category == category)
        result = await session.execute(stmt)
        return result.scalars().all()

async def search_faqs_by_category(category):
    async with async_session_maker() as session:
        if category == "Нет категории":
            stmt = select(FAQ).where(FAQ.category.is_(None))
        else:
            stmt = select(FAQ).where(FAQ.category == category)

        result = await session.execute(stmt)
        faqs = result.scalars().all()
        return faqs

async def find_categories():
    async with async_session_maker() as session:
        result = await session.execute(select(FAQ.category).distinct())
        categories_raw = result.scalars().all()
        return categories_raw
    

async def add_faq_with_excel(df):
    added = 0
    async with async_session_maker() as session:
        for _, row in df.iterrows():
            category = row["category"]
            if category == "-":
                category = None
            faq = FAQ(
                question=row["question"],
                answer=row["answer"],
                category=category,
            )
            session.add(faq)
            added += 1
        await session.commit()
    return added