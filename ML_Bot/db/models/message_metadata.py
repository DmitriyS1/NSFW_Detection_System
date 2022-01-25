from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
from . import Base


class MessageMetadata(Base):
    __tablename__ = "message_metadata"

    id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger)
    msg_id = Column(BigInteger, ForeignKey(
        "message.id"), nullable=True, index=True)
    tg_msg_id = Column(BigInteger, nullable=True, index=True)
    user_id = Column(BigInteger)
    links = relationship("Link", back_populates="message_metadata")
    is_blocked_by_avatar = Column(Boolean)
    is_deleted = Column(Boolean)
