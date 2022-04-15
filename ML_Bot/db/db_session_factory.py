from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import db_config

engine = create_engine(
    'postgresql+psycopg2://nsfw_admin:aHR!##9887ASDsda@database-nsfw-prod.cdlt3gh42ady.eu-west-2.rds.amazonaws.com:5444/NSFWBotDatabase')
# engine = create_engine(
#     'postgresql+psycopg2://back:aHR!##9887ASDsda@localhost:5432/ml_bot')

_SessionFactory = sessionmaker(bind = engine)

Base = declarative_base()

def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()
    