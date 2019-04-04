import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import UnmappedClassError

from app import settings
from .model import BaseQuery, Model


class _QueryProperty:
    def __init__(self, sa):
        self.sa = sa

    def __get__(self, obj, type):
        try:
            mapper = orm.class_mapper(type)
            if mapper:
                return type.query_class(mapper, session=self.sa.session())
        except UnmappedClassError:
            return None


class Database:
    Query = None

    def __init__(
        self,
        session_options=None,
        metadata=None,
        query_class=BaseQuery,
        model_class=Model
    ):

        self.Query = query_class
        self.session = self.create_scoped_session(session_options)
        self.Model = self.make_declarative_base(model_class, metadata)

    @property
    def metadata(self):
        return self.Model.metadata

    def create_scoped_session(self, options=None):
        if options is None:
            options = {}

        options.setdefault('query_cls', self.Query)
        return orm.scoped_session(self.create_session(options))

    def create_session(self, options):
        return orm.sessionmaker(**options, bind=self.engine)

    def make_declarative_base(self, model, metadata=None):
        model = declarative_base(cls=model, name='Model', metadata=metadata)

        if not getattr(model, 'query_class', None):
            model.query_class = self.Query

        model.query = _QueryProperty(self)

        return model

    @property
    def engine(self):
        return sa.create_engine(str(settings.DATABASE_URL))

    def create_all(self):
        self.Model.metadata.create_all(self.engine)

    def drop_all(self):
        self.Model.metadata.drop_all(self.engine)