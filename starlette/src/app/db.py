import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from sqlalchemy.orm import Query, scoped_session, sessionmaker

from app.settings import DATABASE_URL


engine = sa.create_engine(str(DATABASE_URL), convert_unicode=True)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


@as_declarative()
class Base:
    """ Generic declarative base class """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        return f'<{self.__class__.__name__}, id={self.id}>'

    def __str__(self):
        return self.__repr__()

    id = sa.Column(
        sa.Integer,
        primary_key=True
    )

    def save(self):
        """ Save the current object """

        session = Session()

        try:
            session.add(self)
            session.commit()

        except Exception as e:
            session.rollback()
            raise e

    def delete(self):
        """ Delete the current object """

        session = Session()

        try:
            session.delete(self)
            session.commit()

        except Exception as e:
            session.rollback()
            raise e

    query: Query = Session.query_property()
