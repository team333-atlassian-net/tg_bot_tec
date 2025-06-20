import random
from db import async_session_maker
from models import User
from sqlalchemy import select

async def generate_unique_pin():
    async with async_session_maker() as session:
        while True:
            pin = ''.join(random.choices('0123456789', k=random.choice([4, 5])))

            # Проверка, есть ли такой PIN уже
            result = await session.execute(
                select(User).where(User.pin_code == pin)
            )
            if not result.scalar_one_or_none():
                return pin
