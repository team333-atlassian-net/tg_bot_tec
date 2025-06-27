import asyncio
from db import async_session_maker
from models import User


async def add_canteen_info():
    async with async_session_maker() as session:
        new_info = User(
                        tg_id = None,
                        first_name =  "Admin",
                        last_name = "Admin",
                        middle_name = "Admin",
                        pin_code = "11111",
                        admin_rule = True
        )
        session.add(new_info)
        await session.commit()
        print("Админ добавлен")

if __name__ == "__main__":
    asyncio.run(add_canteen_info())
