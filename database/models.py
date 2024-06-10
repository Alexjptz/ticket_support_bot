# Third-party
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import PickleType

# Standard
from uuid import uuid4

# Project
from translations import Language

# Creating a base class for declarative models
base = declarative_base()


def get_uuid() -> str:
    return str(uuid4())[:10]


# WHEN CHANGING CURRENT MODELS DON'T FORGET TO MODIFY update() METHOD IN database.py
class UserModel(base):
    __tablename__ = 'Users'
    id = Column(BigInteger, primary_key=True)
    tg_name = Column(String)
    url_name = Column(String)
    status = Column(String)
    lang = Column(String, default=Language.RU.value)
    current_ticket_id = Column(String, default='')
    mute_time = Column(DateTime, default=None)
    is_banned = Column(Boolean, default=False)
    should_notificate = Column(Boolean, default=True)


class TicketModel(base):
    __tablename__ = 'Tickets'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    manager_id = Column(BigInteger, default=None)
    username = Column(String)
    tg_name = Column(String)
    open_date = Column(DateTime)
    last_modified = Column(DateTime)
    close_date = Column(DateTime, default=None)
    title = Column(String)
    description = Column(String)
    comment = Column(String, default='')
    content = Column(PickleType, default=[])


class PreferenceModel(base):
    __tablename__ = 'Preferences'
    key = Column(String, primary_key=True)
    value = Column(PickleType, default={})