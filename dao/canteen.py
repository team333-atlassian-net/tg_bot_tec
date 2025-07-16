from sqlalchemy import select
from models import Canteen, CanteenMenu
from db import async_session_maker

async def add_canteen_info(start, end, description): 
    async with async_session_maker() as session:
        result = await session.execute(select(Canteen))
        canteen = result.scalars().first()
        if canteen:
            canteen.start_time = start
            canteen.end_time = end
            canteen.description = description
        else:
            canteen = Canteen(start_time=start, end_time=end, description=description)
            session.add(canteen)
        await session.commit()

async def add_canteen_menu_info(date, menu, file_id, file_type: str | None):
    async with async_session_maker() as session:
        result = await session.execute(
            select(CanteenMenu).where(CanteenMenu.date == date)
        )
        existing_menu = result.scalar_one_or_none()

        if existing_menu:
            existing_menu.menu = menu
            existing_menu.file_id = file_id
        else:
            new_menu = CanteenMenu(
                date=date,
                menu=menu,
                file_id=file_id,
                file_type=file_type
            )
            session.add(new_menu)
        await session.commit()

async def get_all_canteen_menu():
    async with async_session_maker() as session:
        result = await session.execute(select(CanteenMenu))
        return result.scalars().all()


async def get_canteen_menu_by_id(menu_id: int):
    async with async_session_maker() as session:
        result = await session.execute(select(CanteenMenu).where(CanteenMenu.id == menu_id))
        return result.scalars().first()


async def get_canteen_info():
    async with async_session_maker() as session:
        result = await session.execute(select(Canteen))
        return result.scalar_one_or_none()