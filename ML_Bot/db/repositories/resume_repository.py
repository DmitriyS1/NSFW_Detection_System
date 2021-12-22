from datetime import datetime, timezone

from sqlalchemy import and_

from db.repositories.models.models import Resume
from db.db_session_factory import session_factory

def is_exist(user_id: int) -> bool:
    session = session_factory()    
    resume = session.query(Resume).filter(and_(Resume.user_id == user_id, Resume.deleted_at == None)).first()
    session.close()
    if(resume is not None):
        return True
    else:
        return False
    

def create(resume: Resume):
    session = session_factory()
    session.add(resume)

    session.commit()
    session.close()


def get(id: int) -> Resume:
    session = session_factory()
    resume = session.query(Resume).filter(Resume.id == id).first()
    session.close()

    return resume


def get_by_user_id(user_id: int) -> Resume:
    session = session_factory()
    resume = session.query(Resume).filter(and_(Resume.user_id == user_id, Resume.deleted_at == None)).first()
    session.close()

    return resume


def delete(id: int):
    session = session_factory()
    resume = session.query(Resume).filter(Resume.id == id).first()
    resume.deleted_at = datetime.now(tz=timezone.utc)

    session.commit()
    session.close()
