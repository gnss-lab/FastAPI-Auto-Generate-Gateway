import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope='module')
def get_db_session():
    def _get_db_session(db_url: str):
        Session: sessionmaker = sessionmaker(
            bind=create_engine(db_url))

        session = Session()

        try:
            yield session
        finally:
            session.close()

    return _get_db_session
