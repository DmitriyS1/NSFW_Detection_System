from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from . import Base


class Admin(Base):
    __tablename__ = "admin"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    personal_chat_id = Column(BigInteger, nullable=False)
    groups = relationship("Group")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
