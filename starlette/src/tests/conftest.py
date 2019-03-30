import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, drop_database
from starlette.config import environ

environ['TESTING'] = 'TRUE'

from app import db, settings


@pytest.fixture(scope="session")
def engine(request):
    url = str(settings.DATABASE_URL)

    engine = create_engine(url)
    create_database(url)

    def fin():
        drop_database(url)

    request.addfinalizer(fin)

    return engine

@pytest.fixture(autouse=True, scope="module")
def create_tables(request, engine):
    db.Base.metadata.create_all(engine)

    def fin():
        db.Base.metadata.drop_all(engine)

    request.addfinalizer(fin)
