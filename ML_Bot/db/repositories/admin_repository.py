from datetime import datetime, timezone
from db.models.admin import Admin
from db.db_session_factory import session_factory
from sqlalchemy import and_


def create(id: int, name: str) -> Admin:
    session = session_factory()
    admin = Admin(
        id=id,
        name=name,
        created_at=datetime.now(tz=timezone.utc)
    )

    session.add(admin)
    session.commit()
    session.refresh(admin)
    session.close()

    return admin


def get(admin_id: int) -> Admin:
    session = session_factory()
    admin = session.query(Admin).filter(Admin.id == admin_id).first()
    session.close()

    return admin
