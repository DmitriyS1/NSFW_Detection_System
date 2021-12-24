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

    # username = Column(String(128), nullable=True) msg msg link link
    # profession = Column(String(128))
    # programming_language = Column(String)
    # resumes = relationship("Resume", back_populates="user")
    # state = relationship("UserState", uselist=False, backref="user_state")

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

class MessageMetadata(Base):
    __tablename__ = "message_metadata"

    id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey("link.id"), nullable=False, index=True)
    chat_id = Column(Integer)
    msg_id = Column(Integer, ForeignKey("message.id"))
    from_user_id = Column(Integer)


class Link(Base):
    __tablename__ = "link"

    id = Column(Integer, primary_key=True)
    link = Column(String, index=True)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)

    # user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    # user = relationship("User", back_populates="resumes")
    # link = Column(String)
    # filename = Column(String)
    # extension = Column(String(8))
    # file_data = Column(BYTEA)


# class UserState(db.Model):
#     __tablename__ = "user_state"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
#     is_questioning = Column(Boolean)
