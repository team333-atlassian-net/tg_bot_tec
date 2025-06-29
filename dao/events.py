from sqlalchemy import select
from db import async_session_maker
from models import Event

async def create_event(title: str, description: str):
    async with async_session_maker() as session:
        event = Event(title=title, description=description)
        session.add(event)
        await session.commit()

async def get_all_events():
    async with async_session_maker() as session:
        res = await session.execute(select(Event))
        return res.scalars().all()