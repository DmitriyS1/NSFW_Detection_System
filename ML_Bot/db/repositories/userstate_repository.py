from db.repositories.models.models import UserState
from db.db_session_factory import session_factory


def change_state(user_id: int, is_questioning: bool):
    session = session_factory()
    state = session.query(UserState).filter(UserState.user_id == user_id).first()
    if state is None:
        session.close()
        return
    
    state.is_questioning = is_questioning
    session.commit()
    session.close()


def get_or_create(user_id: int) -> UserState:
    session = session_factory()
    state = session.query(UserState).filter(UserState.user_id == user_id).first()

    if state is not None:
        return state
        
    new_state = UserState(user_id = user_id, is_questioning = False)
    session.add(new_state)
    session.commit()
    session.refresh(new_state)
    session.close()

    return new_state


def get(user_id: int) -> UserState:
    session = session_factory()
    state = session.query(UserState).filter(UserState.user_id == user_id).first()
    
    session.close()
    return state
