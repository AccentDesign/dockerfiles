import sqlalchemy as sa
from sqlalchemy.orm import Query

from app.db import database


class Foo(database.Model):
    name = sa.Column(sa.String(255), unique=True)


def test_default_tablename():
    assert 'foo' == Foo.__tablename__


def test_default_repr():
    assert '<Foo, id=1>' == Foo(id=1).__repr__()


def test_default_str():
    assert '<Foo, id=1>' == Foo(id=1).__str__()


def test_id(db_session):
    foo = Foo(name='foo')
    db_session.add(foo)
    db_session.flush()

    # foo has an id
    assert foo.id is not None
    # foo can be got with its id
    assert foo == db_session.query(Foo).get(foo.id)


def test_query(db_session):
    db_session.add_all([
        Foo(name='foo'),
        Foo(name='bar'),
    ])
    db_session.flush()

    assert isinstance(Foo.query, Query)

    # just a couple of test queries
    assert 2 == Foo.query.count()
    assert 1 == Foo.query.filter(Foo.name == 'bar').count()
