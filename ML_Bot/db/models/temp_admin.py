from sqlalchemy import BigInteger, Column, DateTime, String
from ML_Bot.db.models import Base


class TempAdmin(Base):
    __tablename__ = "temp_admin"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    personal_chat_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False)
    