import asyncio
from datetime import datetime
from db import async_session_maker
from models import CanteenInfo, User
from sqlalchemy.future import select

FILE_PATH = "files/menu.pdf"
IMAGE_PATH = "images/canteen.jpg"

async def add_canteen_info():
    async with async_session_maker() as session:
        user_dao = await session.execute(
            select(User).where(User.first_name == "Admin", User.last_name == "Admin", User.middle_name == "Admin")
        )
        user = user_dao.scalar_one_or_none()
        new_info = CanteenInfo(
            work_schedule="Пн–Пт: 08:00–18:00",
            menu_text="1. Борщ\n2. Котлета с пюре\n3. Компот",
            file_path=FILE_PATH,
            image_path=IMAGE_PATH,
            created_by=user.id,
            created_at=datetime.utcnow()
        )
        session.add(new_info)
        await session.commit()
        print("✅ Информация о столовой добавлена.")

if __name__ == "__main__":
    asyncio.run(add_canteen_info())
