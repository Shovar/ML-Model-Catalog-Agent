from sqlalchemy.orm import Session

from app.config import settings
from catalogue.schema import get_engine, init_db

engine = get_engine(settings.database_url)
init_db(engine)


def get_session():
    return Session(engine)
