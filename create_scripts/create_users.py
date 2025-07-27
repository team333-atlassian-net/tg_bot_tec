import asyncio
from sqlalchemy import select
from db import async_session_maker
from models import User


async def add_admin():
    async with async_session_maker() as session:
        # Проверка на существование по pin_code
        existing_admin = await session.scalar(
            select(User).where(User.pin_code == "11111")
        )

        if existing_admin:
            print(f"Администратор уже есть")
            return

        new_admin = User(
                        tg_id = None,
                        first_name =  "Admin",
                        last_name = "Admin",
                        middle_name = "Admin",
                        pin_code = "11111",
                        admin_rule = True
        )

        session.add(new_admin)
        await session.commit()
        print("Админ добавлен")


async def add_users():
    users_to_add = [
        {
            "first_name": "Иван",
            "last_name": "Иванов",
            "middle_name": "Иванович",
            "pin_code": "12345",
        },
        {
            "first_name": "Петр",
            "last_name": "Петров",
            "middle_name": "Петрович",
            "pin_code": "23456",
        },
        {
            "first_name": "Анна",
            "last_name": "Смирнова",
            "middle_name": "Александровна",
            "pin_code": "34567",
        },
    ]

    async with async_session_maker() as session:
        for user in users_to_add:
            # Проверка на существование по pin_code
            existing_user = await session.scalar(
                select(User).where(User.pin_code == user["pin_code"])
            )

            if existing_user:
                print(f"Пользователь с пином {user['pin_code']} уже существует. Пропущен.")
                continue

            new_user = User(
                tg_id=None,
                first_name=user["first_name"],
                last_name=user["last_name"],
                middle_name=user["middle_name"],
                pin_code=user["pin_code"],
                admin_rule=False
            )
            session.add(new_user)

        await session.commit()
        print("Пользователи добавлены")

if __name__ == "__main__":
    async def main():
        await add_admin()
        await add_users()

    asyncio.run(main())
