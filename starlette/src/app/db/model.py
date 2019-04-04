import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declared_attr


class BaseQuery(orm.Query):
    pass


class Model:
    #: Query class used by :attr:`query`. Defaults to
    # :class:`SQLAlchemy.Query`, which defaults to :class:`BaseQuery`.
    query_class = None

    #: Convenience property to query the database for instances of this model
    # using the current session. Equivalent to ``db.session.query(Model)``
    # unless :attr:`query_class` has been changed.
    query = None

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        return f'<{self.__class__.__name__}, id={self.id}>'

    def __str__(self):
        return self.__repr__()

    id = sa.Column(sa.Integer, primary_key=True)
