from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from . import Base


class Message(Base):
    __tablename__ = "message"

    id = Column(BigInteger, primary_key=True)
    text = Column(String)
    message_metadata_id = Column(BigInteger, ForeignKey("message_metadata.id"), nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
