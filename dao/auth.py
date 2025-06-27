from sqlalchemy.future import select
from models import User, RegistrationRequest
from db import async_session_maker
from utils.generate_pin import generate_unique_pin

async def get_user(**filters):
    """Функция для поиска пользователя по заданным критериям

    - Пример:
        user = await get_user(pin_code="12341")
        user = await get_user(tg_id="1111111")
    """
    async with async_session_maker() as session:
        query = select(User)
        if filters:
            query = query.filter_by(**filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()

async def get_users(**filters):
    """Функция для поиска пользователей по заданным критериям

    - Пример:
        user = await get_users(pin_code="1234qwe")
        user = await get_users(tg_id="1111111")
    """
    async with async_session_maker() as session:
        query = select(User)
        if filters:
            query = query.filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().all()
    

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
            pin = await generate_unique_pin()
            user = User(
                first_name=row["first_name"],
                last_name=row["last_name"],
                middle_name=row["middle_name"],
                pin_code=pin,
                tg_id=None
            )
            session.add(user)
            added += 1
        await session.commit()
    return added


async def is_admin(tg_id: int) -> bool:
    """Проверяет, что роль - админ"""
    user = await get_user(tg_id=tg_id, admin_rule=True)
    return user is not None


async def create_registration_request(tg_id: str, first_name: str, last_name: str, middle_name: str):
    """Создание заявки на регистрацию"""
    async with async_session_maker() as session:
        request = RegistrationRequest(
            tg_id=tg_id,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
        )
        session.add(request)
        await session.commit()
        return request
    

async def get_request(**filters):
    """Получение заявки"""
    async with async_session_maker() as session:
        query = select(RegistrationRequest)
        if filters:
            query = query.filter_by(**filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()

async def get_pending_requests():
    """Получение всех отправленных заявок"""
    async with async_session_maker() as session:
        result = await session.execute(
            select(RegistrationRequest).where(RegistrationRequest.status == "pending")
        )
        return result.scalars().all()

async def update_request_status(request_id, status):
    """Обновление статуса заявки"""
    async with async_session_maker() as session:
        result = await session.execute(select(RegistrationRequest).where(RegistrationRequest.id == request_id))
        req = result.scalar_one_or_none()
        if req:
            req.status = status
            session.add(req)
            await session.commit()
