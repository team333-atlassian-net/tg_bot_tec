from sqlalchemy import select, or_, update, delete
from models import FAQ, FAQKeyWords
from db import async_session_maker
from sqlalchemy.orm import joinedload
async def add_faq_with_keywords(question: str,
                                answer: str,
                                category: str | None,
                                keywords: list[str]):
    async with async_session_maker() as session:
        faq = FAQ(question=question, answer=answer, category=category)
        session.add(faq)
        await session.flush()

        for word in keywords:
            session.add(FAQKeyWords(faq_id=faq.id, word=word))
        await session.commit()


async def get_all_faq():
    async with async_session_maker() as session:
        res = await session.execute(select(FAQ))
        return res.scalars().all()

async def get_faq_by_id(faq_id: int):
    async with async_session_maker() as session:
        result = await session.execute(
            select(FAQ)
            .options(joinedload(FAQ.keywords))
            .where(FAQ.id == faq_id)
        )
        return result.unique().scalar_one_or_none()
    
# async def update_event(event_id: str, new_title: str | None, new_description: str | None):
#     async with async_session_maker() as session:
#         event = await session.get(Event, event_id)
#         if not event:
#             return
#         if new_title:
#             event.title = new_title
#         if new_description:
#             event.description = new_description
#         await session.commit()


async def get_all_categories():
    async with async_session_maker() as session:
        result = await session.execute(select(FAQ.category).distinct())
        return [r[0] for r in result if r[0]]


async def get_faq_by_category(category: str):
    async with async_session_maker() as session:
        result = await session.execute(
            select(FAQ).where(FAQ.category == category)
        )
        return result.scalars().all()

async def search_faq(query: str) -> list[FAQ]:
    async with async_session_maker() as session:
        q = f"%{query.lower()}%"
        stmt = (
            select(FAQ)
            .outerjoin(FAQKeyWords)
            .where(
                or_(
                    FAQ.question.ilike(q),
                    FAQ.answer.ilike(q),
                    FAQ.category.ilike(q),
                    FAQKeyWords.word.ilike(q),
                )
            )
            .distinct()
        )
        result = await session.execute(stmt)
        return result.scalars().all()
    

async def update_faq(faq_id: int,
                     new_question: str | None,
                     new_answer: str | None,
                     new_category: str | None):
    async with async_session_maker() as session:
        faq = await session.get(FAQ, faq_id)
        if not faq:
            return
        if new_question:
            faq.question = new_question
        if new_answer:
            faq.answer = new_answer
        if new_category:
            faq.category = new_category
        await session.commit()

async def update_key_words(faq_id: int, keywords: list[str]):
    async with async_session_maker() as session:
        # Удалить старые ключевые слова
        await session.execute(
            delete(FAQKeyWords).where(FAQKeyWords.faq_id == faq_id)
        )

        # Добавить новые ключевые слова
        new_keywords = [
            FAQKeyWords(faq_id=faq_id, word=kw.strip())
            for kw in keywords if kw.strip()
        ]
        session.add_all(new_keywords)

        await session.commit()

async def delete_faq(faq_id: int):
    async with async_session_maker() as session:
        # Удаляем ключевые слова, связанные с FAQ
        await session.execute(
            delete(FAQKeyWords).where(FAQKeyWords.faq_id == faq_id)
        )
        # Удаляем сам FAQ
        faq = await session.get(FAQ, faq_id)
        if faq:
            await session.delete(faq)

        await session.commit()
