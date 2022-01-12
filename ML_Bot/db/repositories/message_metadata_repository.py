import typing
from db.db_session_factory import session_factory
from db.models.message_metadata import MessageMetadata

def create(chat_id: int, msg_id: int, tg_msg_id: int, user_id: int) -> MessageMetadata:
    session = session_factory()
    message_metadata = MessageMetadata(
        chat_id = chat_id,
        msg_id = msg_id,
        tg_msg_id = tg_msg_id,
        user_id = user_id)

    session.add(message_metadata)
    session.commit()
    session.refresh(message_metadata)
    session.close()

    return message_metadata
    

def get(id: int) -> MessageMetadata:
    session = session_factory()
    message_metadata = session.query(MessageMetadata).filter(MessageMetadata.id == id).first()
    session.close()

    return message_metadata


def get(msg_id: int) -> MessageMetadata:
    session = session_factory()
    message_metadata = session.query(MessageMetadata).filter(MessageMetadata.msg_id == msg_id).first()
    session.close()

    return message_metadata


def get(chat_id: int) -> typing.List[MessageMetadata]:
    session = session_factory()
    message_metadatas = session.query(MessageMetadata).filter(MessageMetadata.chat_id == chat_id)
    session.close()

    return message_metadatas


def delete(id: int):
    session = session_factory()
    message_metadata = session.query(MessageMetadata).filter(MessageMetadata.id == id).first()
    if message_metadata is not None:
        message_metadata.is_deleted = True
    
    session.commit()
    session.close()