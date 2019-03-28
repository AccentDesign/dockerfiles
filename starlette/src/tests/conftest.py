import pytest
from starlette.config import environ
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

environ['TESTING'] = 'TRUE'

from app import settings
from app import app
from app.db import Base


metadata = Base.metadata


@pytest.fixture(autouse=True, scope="session")
def setup_test_database():
    """
    Create a clean test database every time the tests are run.
    """
    url = str(settings.DATABASE_URL)
    engine = create_engine(url)
    assert not database_exists(url), 'Test database already exists. Aborting tests.'
    create_database(url)             # Create the test database.
    metadata.create_all(engine)      # Create the tables.
    yield                            # Run the tests.
    drop_database(url)               # Drop the test database.


@pytest.fixture()
def client():
    """
    Make a 'client' fixture available to test cases.
    """
    # Our fixture is created within a context manager. This ensures that
    # application startup and shutdown run for every test case.
    #
    # Because we've configured the DatabaseMiddleware with `rollback_on_shutdown`
    # we'll get a complete rollback to the initial state after each test case runs.
    with TestClient(app) as test_client:
        yield test_client

