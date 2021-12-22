from datetime import date

from sqlalchemy.sql.expression import null
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from db.repositories.models.models import User
from db.db_session_factory import session_factory

def create(user: User):
    session = session_factory()
    session.add(user)

    session.commit()
    session.close()


def get(id: int) -> User:
    session = session_factory()
    try:
        user_query = session.query(User).filter(User.id == id).one()
    except MultipleResultsFound as e:
        print(e)
        # LOGGING! e.with_traceback()
    except NoResultFound as e:
        print(e)
        return None
    finally:
        session.close()

    return user_query
