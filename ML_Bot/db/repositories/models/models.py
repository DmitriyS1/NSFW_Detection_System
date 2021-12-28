from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime

Base = declarative_base()

class Message(Base):
    __tablename__ = "message"

    id = Column(BigInteger, primary_key=True)
    text = Column(String)
    message_metadata = relationship("MessageMetadata", back_populates="message", uselist=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)


class MessageMetadata(Base):
    __tablename__ = "message_metadata"

    id = Column(BigInteger, primary_key=True)
    chat_id = Column(BigInteger)
    msg_id = Column(BigInteger, ForeignKey("message.id"), nullable=False, index=True)
    tg_msg_id = Column(BigInteger, nullable=True, index=True)
    message = relationship("Message", back_populates="message_metadata")
    user_id = Column(BigInteger)
    links = relationship("Link", back_populates="message_metadata")
    is_deleted = Column(Boolean)


class Link(Base):
    __tablename__ = "link"

    id = Column(BigInteger, primary_key=True)
    message_metadata_id = Column(BigInteger, ForeignKey("message_metadata.id"), nullable=False)
    message_metadata = relationship("MessageMetadata", back_populates="links")
    link = Column(String, index=True)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
