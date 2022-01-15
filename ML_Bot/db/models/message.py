from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from . import Base


class Message(Base):
    __tablename__ = "message"

    id = Column(BigInteger, primary_key=True)
    text = Column(String)
    message_metadata_id = Column(BigInteger, ForeignKey("message_metadata.id"), nullable=False)
    message_metadata = relationship(
        "MessageMetadata", back_populates="message")
    is_blocked_by_avatar = Column(Boolean)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
