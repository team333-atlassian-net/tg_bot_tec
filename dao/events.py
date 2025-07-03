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

async def get_event_by_id(event_id: int):
    async with async_session_maker() as session:
        res = await session.execute(select(Event).where(Event.id == event_id))
        return res.scalars().all()
    
async def update_event(event_id: str, new_title: str, new_description: str):
    async with async_session_maker() as session:
        event = await session.get(Event, event_id)
        if event:
            event.title = new_title
            event.description = new_description
            await session.commit()

async def delete_event(event_id: str):
    async with async_session_maker() as session:
        event = await session.get(Event, event_id)
        if event:
            await session.delete(event)
            await session.commit()
