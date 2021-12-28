from datetime import datetime, timezone
from db.db_session_factory import session_factory
from db.repositories.models.models import Message
from sqlalchemy import and_

def create(text: str) -> Message:
    session = session_factory()
    message = Message(
        text = text,
        created_at = datetime.now(tz=timezone.utc))

    session.add(message)
    session.commit()
    session.refresh(message)
    session.close()

    return message
    

def get(id: int) -> Message:
    session = session_factory()
    message = session.query(Message).filter(and_(Message.id == id, Message.deleted_at == None)).first()
    session.close()

    return message


def delete(id: int):
    session = session_factory()
    message = session.query(Message).filter(Message.id == id).first()
    if message is not None:
        message.deleted_at = datetime.now(tz=timezone.utc)
    
    session.commit()
    session.close()