from sqlalchemy.future import select
from models import CanteenInfo
from db import async_session_maker

async def get_latest_canteen_info() -> CanteenInfo | None:
    """Получение информации о столовой"""
    async with async_session_maker() as session:
        result = await session.execute(
            select(CanteenInfo).order_by(CanteenInfo.created_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()
