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
        is_moderation_active=False
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

