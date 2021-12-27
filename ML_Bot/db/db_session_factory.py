from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://back:aHR!##9887ASDsda@bot_database:5432/ml_bot',
    connect_args={"check_same_thread": False})

_SessionFactory = sessionmaker(bind = engine)

Base = declarative_base()

def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()
    