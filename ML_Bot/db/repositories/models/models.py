from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.sql.sqltypes import Boolean, DateTime

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    username = Column(String(128), nullable=True)
    profession = Column(String(128))
    programming_language = Column(String)
    resumes = relationship("Resume", back_populates="user")
    state = relationship("UserState", uselist=False, backref="user_state")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)


class Resume(Base):
    __tablename__ = "resume"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="resumes")
    link = Column(String)
    filename = Column(String)
    extension = Column(String(8))
    file_data = Column(BYTEA)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)

class UserState(Base):
    __tablename__ = "user_state"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    is_questioning = Column(Boolean)
