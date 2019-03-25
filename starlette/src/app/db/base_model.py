from sqlalchemy import Column, Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session

from app.db import SessionLocal


@as_declarative()
class Base:
    """ Generic declarative base class """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(
        Integer,
        primary_key=True
    )

    def __repr__(self):
        return f'<{self.__class__.__name__}, id={self.id}>'

    def __str__(self):
        return self.__repr__()

    def save(self, session: Session = None):
        """
        Saves the current object

        :param session: An optional instance if a sqlalchemy session to use.
        """

        has_session = session is not None

        if not has_session:
            session = SessionLocal()

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
