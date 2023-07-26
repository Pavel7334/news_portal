from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, ForeignKey

metadata = MetaData()

Base = declarative_base()


class Role(Base):
    __tablename__ = 'role'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    permissions = sa.Column(sa.JSON)


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, nullable=False)
    username = sa.Column(sa.String, nullable=False)
    registered_at = sa.Column(sa.TIMESTAMP, default=datetime.utcnow)
    role_id = sa.Column(sa.Integer, ForeignKey('role.id'))
    hashed_password = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    is_superuser = sa.Column(sa.Boolean, default=False, nullable=False)
    is_verified = sa.Column(sa.Boolean, default=False, nullable=False)


class News(Base):
    __tablename__ = 'news'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    published_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    is_draft = sa.Column(sa.Boolean, default=True, nullable=False)
    user_id = sa.Column(sa.Integer, ForeignKey('user.id'))
