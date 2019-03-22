from sqlalchemy import Column, String

from .base import Base


class Group(Base):
    __tablename__ = 'groups'

    name = Column(
        String(255),
        unique=True,
        nullable=False
    )

    def __str__(self):
        return self.name
