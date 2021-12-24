from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.sql.sqltypes import Boolean, DateTime

Base = declarative_base()

class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    message_metadata = relationship("MessageMetadata", back_populates="message", uselist=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)


class MessageMetadata(Base):
    __tablename__ = "message_metadata"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    msg_id = Column(Integer, ForeignKey("message.id"), nullable=False, index=True)
    message = relationship("Message", back_populates="message_metadata")
    user_id = Column(Integer)
    links = relationship("Link", back_populates="message_metadata")


class Link(Base):
    __tablename__ = "link"

    id = Column(Integer, primary_key=True)
    message_metadata_id = Column(Integer, ForeignKey("message_metadata.id"), nullable=False)
    message_metadata = relationship("MessageMetadata", back_populates="links")
    link = Column(String, index=True)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
