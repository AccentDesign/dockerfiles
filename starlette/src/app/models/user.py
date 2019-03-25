import binascii
import hashlib
import os

from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType

from .base import Base

user_groups = Table(
    'user_groups',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('group_id', ForeignKey('groups.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    email = Column(
        EmailType,
        index=True,
        unique=True
    )
    password = Column(
        String(255)
    )
    first_name = Column(
        String(120)
    )
    last_name = Column(
        String(120)
    )
    groups = relationship(
        "Group",
        secondary=user_groups,
        backref="users"
    )

    def __str__(self):
        return self.email

    @property
    def display_name(self):
        return f'{self.first_name} {self.last_name}'

    def set_password(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        password_hash = hashlib.pbkdf2_hmac(
            'sha512',
            password.encode('utf-8'),
            salt,
            100000
        )
        password_hash = binascii.hexlify(password_hash)
        self.password = (salt + password_hash).decode('ascii')

    def check_password(self, password):
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
