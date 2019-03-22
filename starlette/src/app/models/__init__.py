from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import settings


engine = create_engine(str(settings.DATABASE_URL))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = SessionLocal()


from .base import Base
from .group import *
from .user import *
