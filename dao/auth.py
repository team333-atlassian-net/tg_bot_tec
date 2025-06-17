from sqlalchemy.future import select
from models import User
from db import async_session_maker


async def get_user(**filters):
    """Функция для поиска по заданным критериям

    - Пример:
        user = await get_user(pin_code="1234qwe")
        user = await get_user(tg_id="1111111")
    """
    async with async_session_maker() as session:
        query = select(User)
        if filters:
            query = query.filter_by(**filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def update_or_add_tg_id(user, tg_id):
    """Функция для обновления или добавления tg_id для пользователя"""
    async with async_session_maker() as session:
        user.tg_id = tg_id
        session.add(user)
        await session.commit()

async def add_user(user):
    """Добавляет пользователя в БД"""
    async with async_session_maker() as session:
        session.add(user)
        await session.commit()

async def add_user_with_excel(df):
    """Добавляет пользователя в БД из excel файла"""
    added = 0
    async with async_session_maker() as session:
        for _, row in df.iterrows():
            exists = await session.execute(select(User).where(User.pin_code == str(row["pin_code"])))
            if exists.scalar_one_or_none():
                continue  # пропустить дубли
            user = User(
                first_name=row["first_name"],
                last_name=row["last_name"],
                middle_name=row["middle_name"],
                pin_code=str(row["pin_code"]),
                tg_id=None
            )
            session.add(user)
            added += 1
        await session.commit()
    return added
