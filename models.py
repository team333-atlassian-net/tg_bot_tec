import uuid
from db import Base
from sqlalchemy import Column, BigInteger, String, Boolean, Integer, Text, TIMESTAMP, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

class User(Base):
    """Пользователи"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    tg_id = Column(BigInteger, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    pin_code = Column(String, unique=True, nullable=False)
    admin_rule = Column(Boolean, nullable=False, default=False)

class CompanyInfo(Base):
    """Информация о компании"""
    __tablename__ = 'company_info'

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text)
    file_path = Column(Text)
    image_path = Column(Text)
    created_by = Column(UUID, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP)


class FAQ(Base):
    """Вопросы и ответы"""
    __tablename__ = 'faq'

    id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    category = Column(Text)
    created_by = Column(UUID, ForeignKey('users.id'))


class DocumentInstruction(Base):
    """Инструкции"""
    __tablename__ = 'document_instructions'

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    instructions = Column(Text)
    file_path = Column(Text)


class Feedback(Base):
    """Отзывы о боте"""
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID, ForeignKey('users.id'))
    text = Column(Text)
    is_anonymous = Column(Boolean)
    created_at = Column(TIMESTAMP)


class CanteenInfo(Base):
    """Модель столовой"""
    __tablename__ = 'canteen_info'

    id = Column(Integer, primary_key=True)
    work_schedule = Column(Text)
    menu_text = Column(Text)
    file_path = Column(Text)  # PDF или изображение
    image_path = Column(Text)
    created_by = Column(UUID, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP)


class RegistrationRequest(Base):
    __tablename__ = "registration_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tg_id = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, approved, rejected
    created_at = Column(TIMESTAMP)