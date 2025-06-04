from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

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

    def __repr__(self):
        return f"<User(full_name='{self.first_name} {self.last_name} {self.middle_name}', telegram_id={self.tg_id}, admin_rule={self.admin_rule})>"
