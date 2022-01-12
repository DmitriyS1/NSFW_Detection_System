from datetime import datetime, timezone
from db.db_session_factory import session_factory
from db.models.link import Link
from sqlalchemy import and_

def create(message_metadata_id: int, link_text: str) -> Link:
    session = session_factory()
    link = Link(
        message_metadata_id = message_metadata_id, 
        link = link_text,
        created_at = datetime.now(tz=timezone.utc))

    session.add(link)
    session.commit()
    session.refresh(link)
    session.close()

    return link
    

def get(link_id: int) -> Link:
    session = session_factory()
    link = session.query(Link).filter(and_(Link.id == link_id, Link.deleted_at == None)).first()
    session.close()

    return link


def get(link: str) -> Link:
    session = session_factory()
    link = session.query(Link).filter(and_(Link.link == link, Link.deleted_at == None)).first()
    session.close()

    return link


def delete(link_id: int):
    session = session_factory()
    link = session.query(Link).filter(Link.id == link_id).first()
    if link is not None:
        link.deleted_at = datetime.now(tz=timezone.utc)
    
    session.commit()
    session.close()
