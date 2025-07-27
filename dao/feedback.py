from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.future import select
from uuid import UUID
from typing import List, Optional
from db import async_session_maker

from models import Feedback, FeedbackAttachments


async def create_feedback(
    user_id: UUID,
    text: str,
) -> Feedback:
    async with async_session_maker() as session:
        feedback = Feedback(user_id=user_id, text=text)
        session.add(feedback)
        await session.commit()
        await session.refresh(feedback)
        return feedback


async def add_feedback_attachment(feedback_id: int, file_id: str) -> None:
    async with async_session_maker() as session:
        attachment = FeedbackAttachments(feedback_id=feedback_id, file_id=file_id)
        session.add(attachment)
        await session.commit()


async def get_attachments_by_feedback_id(feedback_id: int) -> list[FeedbackAttachments]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(FeedbackAttachments).where(
                FeedbackAttachments.feedback_id == feedback_id
            )
        )
        return result.scalars().all()


async def get_attachment_by_id(id: int) -> FeedbackAttachments:
    async with async_session_maker() as session:
        result = await session.execute(
            select(FeedbackAttachments).where(FeedbackAttachments.id == id)
        )
        return result.scalar_one_or_none()


async def get_feedback_by_id(feedback_id: int) -> Optional[Feedback]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(Feedback).where(Feedback.id == feedback_id)
        )
        return result.scalar_one_or_none()


async def get_feedbacks_by_user(user_id: UUID) -> List[Feedback]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(Feedback).where(Feedback.user_id == user_id)
        )
        return result.scalars().all()


async def get_unread_feedbacks() -> List[Feedback]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(Feedback).where(Feedback.is_read == False)
        )
        feedbacks = result.scalars().all()
        return feedbacks


async def get_feedbacks(**filters) -> List[Feedback]:
    async with async_session_maker() as session:
        query = select(Feedback)
        if filters:
            query = query.filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()


async def get_all_feedbacks() -> List[Feedback]:
    async with async_session_maker() as session:
        result = await session.execute(select(Feedback))
        feedbacks = result.scalars().all()
    return feedbacks


async def mark_feedback_as_read(feedback_id: int) -> None:
    async with async_session_maker() as session:
        await session.execute(
            update(Feedback)
            .where(Feedback.id == feedback_id)
            .values(is_read=True)
            .execution_options(synchronize_session="fetch")
        )
        await session.commit()


async def delete_feedback(feedback_id: int) -> None:
    async with async_session_maker() as session:
        await session.execute(delete(Feedback).where(Feedback.id == feedback_id))
        await session.commit()
