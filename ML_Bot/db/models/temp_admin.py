from sqlalchemy import BigInteger, Boolean, Column, DateTime, String
from . import Base


class TempAdmin(Base):
    __tablename__ = "temp_admin"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(128))
    chat_id = Column(BigInteger, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False)
