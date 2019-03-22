from sqlalchemy import Column, Integer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from app.models import SessionLocal


class Base:
    """ Generic declarative base class """

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}, id={self.id}>'

    def __str__(self):
        return self.__repr__()

    def save(self, session: Session = None):
        """
        Saves the current object

        :param session: An optional instance if a sqlalchemy session to use.
        """

        sess = session or SessionLocal()

        try:
            # commit and return a fresh copy from the db
            sess.add(self)
            sess.commit()
            return sess.query(self.__class__).get(self.id)

        except IntegrityError as e:
            # oops, rollback and re raise the exception
            sess.rollback()
            raise e

        finally:
            # close the session if it got created here
            if not session:
                sess.close()


Base = declarative_base(cls=Base)
