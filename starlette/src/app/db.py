import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from sqlalchemy.orm import Session, Query, scoped_session, sessionmaker

from app.settings import DATABASE_URL


engine = sa.create_engine(str(DATABASE_URL), convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


@as_declarative()
class Base:
    """ Generic declarative base class """

    def __str__(self):
        return self.__repr__()

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        return f'<{self.__class__.__name__}, id={self.id}>'

    id = sa.Column(
        sa.Integer,
        primary_key=True
    )

    def session(self) -> Session:
        """ Returns a db session for the instance """

        if not hasattr(self, '_session'):
            setattr(self, '_session', db_session())
        return getattr(self, '_session')

    def save(self, session: Session = None):
        """ Saves the current object """

        has_session = session is not None

        if not has_session:
            session = self.session()

        try:
            # commit and return a fresh copy from the db
            session.add(self)
            session.commit()
            return session.query(self.__class__).get(self.id)

        except IntegrityError as e:
            # oops, rollback and re raise the exception
            session.rollback()
            raise e

        finally:
            # close the session if it got created here
            if not has_session:
                session.close()

    """ Returns a query object with a scoped session. eg: MyClass.query.get(1) """
    query: Query = db_session.query_property()
