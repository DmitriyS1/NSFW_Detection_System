from datetime import datetime, timezone
from db.db_session_factory import session_factory
from db.models.group import Group
from sqlalchemy import and_

def create(chat_id: int, admin_id: int, name: str) -> Group:
    '''
    Returns - added Chat object
    '''
    session = session_factory()
    chat = Group(
        id=chat_id,
        admin_id=admin_id,
        name=name,
        is_moderation_active=False,
        created_at=datetime.now(tz=timezone.utc)
    )

    session.add(chat)
    session.commit()
    session.refresh(chat)

    return chat


def get(id: int) -> Group:
    '''
    Returns - found Chat or None
    '''
    session = session_factory()
    chat = session.query(Group).filter(Group.id==id).first()
    session.close()

    return chat

def update(id: int, new_admin_id: int) -> Group:
    '''
    Returns - updated Chat object
    '''
    session = session_factory()
    chat = session.query(Group).filter(Group.id==id).first()
    chat.admin_id = new_admin_id
    session.commit()
    session.refresh(chat)

    return chat

def is_exists(id: int) -> bool:
    '''
    Returns - True if Chat exists
    '''
    session = session_factory()
    chat = session.query(Group).filter(Group.id==id).first()
    session.close()

    return chat is not None
