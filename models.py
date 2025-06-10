from sqlalchemy import Column, BigInteger, String, Boolean, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from config import settings
from sqlalchemy.ext.asyncio import create_async_engine
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    tg_id = Column(BigInteger, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    pin_code = Column(String, unique=True, nullable=False)
    admin_rule = Column(Boolean, nullable=False, default=False)

class CompanyInfo(Base):
    __tablename__ = 'company_info'

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    content = Column(Text)
    file_path = Column(Text)
    image_path = Column(Text)
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP)


class FAQ(Base):
    __tablename__ = 'faq'

    id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    category = Column(Text)
    created_by = Column(Integer, ForeignKey('users.id'))


class DocumentInstruction(Base):
    __tablename__ = 'document_instructions'

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    instructions = Column(Text)
    file_path = Column(Text)


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
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
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(TIMESTAMP)

engine = create_async_engine(settings.DATABASE_URL)  # движок
   