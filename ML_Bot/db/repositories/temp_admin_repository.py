from datetime import datetime, timezone
from typing import List
from db.models.temp_admin import TempAdmin
from db.db_session_factory import session_factory


def create(admin_id: int, name: str, chat_id: int) -> TempAdmin:
    '''
    Returns - added TempAdmin object
    '''
    session = session_factory()
    temp_admin = TempAdmin(
        id=admin_id,
        name=name,
        chat_id=chat_id,
        is_active=False,
        created_at=datetime.now(tz=timezone.utc)
    )

    session.add(temp_admin)
    session.commit()
    session.refresh(temp_admin)

    return temp_admin


def get_inactive_admins() -> List[TempAdmin]:
    '''
    Returns - found TempAdmins or None
    '''
    session = session_factory()
    temp_admins = session.query(TempAdmin).filter(TempAdmin.is_active==False).all()
    session.close()

    return temp_admins


def get(admin_id: int) -> TempAdmin:
    '''
    Returns - found TempAdmin or None
    '''
    session = session_factory()
    temp_admin = session.query(TempAdmin).filter(TempAdmin.id==admin_id).first()
    session.close()

    return temp_admin