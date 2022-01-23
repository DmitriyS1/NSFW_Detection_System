from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from . import Base


class Group(Base):
    __tablename__ = "group"

    id = Column(BigInteger, primary_key=True)
    admin_id = Column(BigInteger, ForeignKey("admin.id"), index=True,)
    is_moderation_active = Column(Boolean, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, nullable=False)
