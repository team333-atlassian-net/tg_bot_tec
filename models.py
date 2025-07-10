import uuid
from db import Base
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    Integer,
    Text,
    TIMESTAMP,
    ForeignKey,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


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

    __tablename__ = "company_info"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text)
    file_path = Column(Text)
    image_path = Column(Text)


class FAQ(Base):
    """Вопросы и ответы"""

    __tablename__ = "faq"

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(Text, nullable=True)


class Feedback(Base):
    """Отзывы о боте"""

    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"))
    text = Column(Text)
    is_anonymous = Column(Boolean)


class RegistrationRequest(Base):
    __tablename__ = "registration_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tg_id = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, approved, rejected


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)


class VirtualExcursion(Base):
    __tablename__ = "virtual_excursions"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    materials = relationship(
        "ExcursionMaterial", back_populates="excursion", cascade="all, delete-orphan"
    )


class ExcursionMaterial(Base):
    __tablename__ = "excursion_materials"

    id = Column(Integer, primary_key=True)
    excursion_id = Column(
        Integer, ForeignKey("virtual_excursions.id", ondelete="CASCADE"), nullable=False
    )
    telegram_file_id = Column(String, nullable=False)
    file_name = Column(String, nullable=True)
    text = Column(String, nullable=True)

    excursion = relationship("VirtualExcursion", back_populates="materials")
