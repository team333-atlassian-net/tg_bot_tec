from datetime import time, date
from sqlalchemy import select, asc
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

async def update_canteen_info(start: time = None,
                              end: time = None,
                              description: str = None):
    async with async_session_maker() as session:
        result = await session.execute(select(Canteen))
        canteen = result.scalars().first()
        if canteen:
            if start is not None:
                canteen.start_time = start
            if end is not None:
                canteen.end_time = end
            if description is not None:
                canteen.description = description
            await session.commit()

async def update_canteen_menu(menu_id: int,
                              date: time = None,
                              menu: time = None,
                              file_id: str = None,
                              file_type: str = None):
    async with async_session_maker() as session:
        result = await session.execute(select(CanteenMenu).where(CanteenMenu.id == menu_id))
        canteen_menu = result.scalars().first()
        if canteen_menu:
            if date is not None:
                canteen_menu.date = date
            if menu is not None:
                canteen_menu.menu = menu
            if file_id is not None:
                canteen_menu.file_id = file_id
            if file_type is not None:
                canteen_menu.file_type = file_type
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
        result = await session.execute(
            select(CanteenMenu).order_by(asc(CanteenMenu.date))
        )
        return result.scalars().all()

async def get_canteen_menu_by_week():
    today = date.today()

    async with async_session_maker() as session:
        result = await session.execute(
            select(CanteenMenu)
            .where(CanteenMenu.date >= today)
            .order_by(asc(CanteenMenu.date))
        )
        return result.scalars().all()
    
async def get_canteen_menu_by_id(menu_id: int):
    async with async_session_maker() as session:
        result = await session.execute(select(CanteenMenu).where(CanteenMenu.id == menu_id))
        return result.scalars().first()

async def get_canteen_menu_by_date(date):
    async with async_session_maker() as session:
        result = await session.execute(select(CanteenMenu).where(CanteenMenu.date == date))
        return result.scalars().first()

async def get_canteen_info():
    async with async_session_maker() as session:
        result = await session.execute(select(Canteen))
        return result.scalar_one_or_none()
    
async def delete_canteen_info():
    async with async_session_maker() as session:
        result = await session.execute(select(Canteen))
        info = result.scalars().first()
        if info:
            await session.delete(info)
            await session.commit()
            
async def delete_canteen_menu_file(menu_id: int):
    async with async_session_maker() as session:
        result = await session.execute(select(Canteen).where(CanteenMenu.id == menu_id))
        canteen_menu = result.scalars().first()
        if canteen_menu:
            canteen_menu.file_id = None
            canteen_menu.file_type = None
            await session.commit()

async def delete_canteen_menu(menu_id: int):
    async with async_session_maker() as session:
        menu = await session.get(CanteenMenu, menu_id)
        if menu:
            await session.delete(menu)
            await session.commit()