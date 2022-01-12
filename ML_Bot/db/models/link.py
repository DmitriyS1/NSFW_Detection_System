from sqlalchemy.orm import relationship
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from . import Base

class Link(Base):
    __tablename__ = "link"

    id = Column(BigInteger, primary_key=True)
    message_metadata_id = Column(BigInteger, ForeignKey(
        "message_metadata.id"), nullable=False)
    message_metadata = relationship("MessageMetadata", back_populates="links")
    link = Column(String, index=True)
    created_at = Column(DateTime, nullable=False)
    deleted_at = Column(DateTime)
