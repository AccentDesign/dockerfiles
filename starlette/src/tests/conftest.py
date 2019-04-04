import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.config import environ


environ['TESTING'] = 'TRUE'


from app import db, settings


@pytest.fixture(scope="session")
def engine(request):
    url = str(settings.DATABASE_URL)

    if database_exists(url):
        drop_database(url)

    engine = create_engine(url)
    create_database(url)

    def fin():
        drop_database(url)

    request.addfinalizer(fin)

    return engine


@pytest.yield_fixture(scope="session")
def tables(engine):
    db.database.create_all()
    yield
    db.database.drop_all()


@pytest.yield_fixture(autouse="true", scope="function")
def db_session(tables):
    session = db.database.session

    yield session

    session.remove()
