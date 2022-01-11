from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from . import Base


class Chat(Base):
    __tablename__ = "chat"

    id = Column(BigInteger, primary_key=True)
    admin_id = Column(BigInteger, index=True)
    is_moderation_active = Column(Boolean, nullable=False)
    name = Column(String)
    