import binascii
import hashlib
import os

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from app.db import Base


user_groups = sa.Table(
    'user_groups',
    Base.metadata,
    sa.Column('user_id', sa.ForeignKey('users.id'), primary_key=True),
    sa.Column('group_id', sa.ForeignKey('groups.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    email = sa.Column(
        EmailType,
        nullable=False,
        index=True,
        unique=True
    )
    password = sa.Column(
        sa.String(255)
    )
    first_name = sa.Column(
        sa.String(120)
    )
    last_name = sa.Column(
        sa.String(120)
    )
    is_active = sa.Column(
        sa.Boolean,
        nullable=False,
        default=True
    )
    groups = relationship(
        'Group',
        secondary=user_groups,
        backref='users'
    )

    def __str__(self):
        return self.email

    @property
    def is_authenticated(self) -> bool:
        return self.is_active
    
    @property
    def display_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def set_password(self, password) -> None:
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        password_hash = hashlib.pbkdf2_hmac(
            'sha512',
            password.encode('utf-8'),
            salt,
            100000
        )
        password_hash = binascii.hexlify(password_hash)
        self.password = (salt + password_hash).decode('ascii')

    def check_password(self, password) -> bool:
        salt = self.password[:64]
        stored_password = self.password[64:]
        password_hash = hashlib.pbkdf2_hmac(
            'sha512',
            password.encode('utf-8'),
            salt.encode('ascii'),
            100000
        )
        password_hash = binascii.hexlify(password_hash).decode('ascii')
        return password_hash == stored_password


class Group(Base):
    __tablename__ = 'groups'

    name = sa.Column(
        sa.String(255),
        unique=True,
        nullable=False
    )

    def __str__(self):
        return self.name
