from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from . import Base


class MessageMetadata(Base):
    __tablename__ = "message_metadata"

    id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger)
    msg_id = Column(BigInteger, ForeignKey(
        "message.id"), nullable=False, index=True)
    tg_msg_id = Column(BigInteger, nullable=True, index=True)
    message = relationship("Message", back_populates="message_metadata")
    user_id = Column(BigInteger)
    links = relationship("Link", back_populates="message_metadata")
    is_deleted = Column(Boolean)
