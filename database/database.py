# Third-party
import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

# Standard
from time import sleep
import traceback
from enum import Enum
from datetime import datetime, timezone, timedelta
import os
import shutil

# Project
import config as cf
from logger import database_logger
from .models import base, UserModel, TicketModel, PreferenceModel


# Enum for different types of database connections
class Type(Enum):
    POSTGRESQL = f'postgresql+psycopg2://{cf.database["user"]}:{cf.database["password"]}@{cf.database["host"]}:{cf.database["port"]}'


class Database:
    # Private method to connect to the database
    def __connect_to_database(self, type_: Type):
        while True:
            database_logger.warning('Connecting to database...')
            try:
                # Creating a database engine
                self.engine = create_engine(type_.value)
                self.session_maker = sessionmaker(bind=self.engine)
                # Creating tables defined in 'base' metadata
                base.metadata.create_all(self.engine)

                # __connect_inner_classes__ !DO NOT DELETE!

                self.users = self.User(session_maker=self.session_maker)
                self.tickets = self.Ticket(session_maker=self.session_maker)
                self.preferences = self.Preference(session_maker=self.session_maker)

                database_logger.info('Connected to database')
                break
            except sqlalchemy.exc.OperationalError:
                # Handling database connection errors
                database_logger.error('Database error:\n' + traceback.format_exc())
                sleep(5.0)

    # Constructor to initialize the Database class
    def __init__(self, type_: Type):
        self.__connect_to_database(type_=type_)

    # __inner_classes__ !DO NOT DELETE!
    class User:
        def __init__(self, session_maker):
            self.session_maker = session_maker

        async def insert(self, user: UserModel):
            with self.session_maker() as session:
                session.add(user)
                session.commit()
                database_logger.info(f'UserModel is created!')
                session.close()

        async def get_all(self) -> list[UserModel] | None:
            with self.session_maker() as session:
                data = session.query(UserModel).all()
                if data:
                    database_logger.info('Fetched all UserModels')
                    return data
                else:
                    database_logger.info('No UserModels in a database')
                    return None

        async def get_all_muted(self) -> list[UserModel] | None:
            with self.session_maker() as session:
                data = session.query(UserModel).filter(UserModel.mute_time.isnot(None)).all()
                if data:
                    database_logger.info('Fetched all muted UserModels')
                    return data
                else:
                    database_logger.info('No muted UserModels in a database')
                    return None

        async def get_all_managers(self) -> list[UserModel] | None:
            with self.session_maker() as session:
                data = session.query(UserModel).filter_by(status='manager').all()
                if data:
                    database_logger.info('Fetched all muted UserModels')
                    return data
                else:
                    database_logger.info('No muted UserModels in a database')
                    return None

        async def get_by_id(self, user_id: int) -> UserModel | None:
            with self.session_maker() as session:
                data = session.query(UserModel).filter_by(id=user_id).first()
                if data:
                    database_logger.info(f'UserModel {user_id} is retrieved from database')
                    session.close()
                    return data
                else:
                    database_logger.info(f'UserModel {user_id} is not in database')
                    session.close()
                    return None

        async def get_by_tg_name(self, tg_name: str) -> UserModel | None:
            with self.session_maker() as session:
                data = session.query(UserModel).filter_by(tg_name=tg_name).first()
                if data:
                    database_logger.info(f'UserModel {tg_name} is retrieved from database')
                    session.close()
                    return data
                else:
                    database_logger.info(f'UserModel {tg_name} is not in database')
                    session.close()
                    return None

        async def get_by_url_name(self, url_name: str) -> UserModel | None:
            with self.session_maker() as session:
                data = session.query(UserModel).filter_by(url_name=url_name).first()
                if data:
                    database_logger.info(f'UserModel {url_name} is retrieved from database')
                    session.close()
                    return data
                else:
                    database_logger.info(f'UserModel {url_name} is not in database')
                    session.close()
                    return None

        async def delete(self, user: UserModel):
            with self.session_maker() as session:
                session.query(UserModel).filter_by(id=user.id).delete()
                database_logger.warning(f'UserModel {user.id} is deleted!')
                session.commit()
                session.close()

        async def update(self, user: UserModel):
            with self.session_maker() as session:
                session.query(UserModel).filter_by(id=user.id).update({
                    'tg_name': user.tg_name,
                    'url_name': user.url_name,
                    'status': user.status,
                    'lang': user.lang,
                    'current_ticket_id': user.current_ticket_id,
                    'mute_time': user.mute_time,
                    'is_banned': user.is_banned,
                    'should_notificate': user.should_notificate
                })
                database_logger.warning(f'UserModel {user.id} is updated!')
                session.commit()
                session.close()

    class Ticket:
        def __init__(self, session_maker):
            self.session_maker = session_maker

        async def insert(self, ticket: TicketModel) -> int:
            with self.session_maker() as session:
                session.add(ticket)
                session.commit()
                ticket_id = ticket.id
                database_logger.info(f'TicketModel is created!')
                session.close()
                return ticket_id

        async def get_all(self) -> list[TicketModel] | None:
            with self.session_maker() as session:
                data = session.query(TicketModel).order_by(desc(TicketModel.id)).all()
                if data:
                    database_logger.info('Fetched all TicketModels')
                    return data
                else:
                    database_logger.info('No TicketModels in a database')
                    return None

        async def get_by_id(self, ticket_id: str | int) -> TicketModel | None:
            with self.session_maker() as session:
                data = session.query(TicketModel).filter_by(id=int(ticket_id)).first()
                if data:
                    database_logger.info(f'TicketModel {ticket_id} is retrieved from database')
                    session.close()
                    return data
                else:
                    database_logger.info(f'TicketModel {ticket_id} is not in database')
                    session.close()
                    return None

        async def get_all_opened(self) -> list[TicketModel] | None:
            with self.session_maker() as session:
                data = session.query(TicketModel).filter_by(close_date=None, manager_id=None).order_by(desc(TicketModel.id)).all()
                if data:
                    database_logger.info('Fetched all opened TicketModels')
                    return data
                else:
                    database_logger.info('No opened TicketModels in a database')
                    return None

        async def get_all_by_id(self, user_id: int, is_manager: bool) -> list[TicketModel] | None:
            with self.session_maker() as session:
                if is_manager:
                    data = session.query(TicketModel).filter_by(manager_id=user_id).order_by(desc(TicketModel.id)).all()
                else:
                    data = session.query(TicketModel).filter_by(user_id=user_id).order_by(desc(TicketModel.id)).all()
                if data:
                    database_logger.info(f'Fetched all TicketModels with user/manager id {user_id}')
                    return data
                else:
                    database_logger.info(f'No TicketModels in a database with user/manager id {user_id}')
                    return None

        async def get_tickets_last_modified_ago(self, time_ago: int, is_hours=True) -> list[TicketModel] | None:
            with self.session_maker() as session:
                data = session.query(TicketModel).filter_by(close_date=None, manager_id=None).all()
                if data:
                    current_time = datetime.now(timezone(timedelta(hours=3)))

                    result = []
                    for ticket in data:
                        last_modified = str(ticket.last_modified).split('.')[0]
                        last_modified_date = datetime.strptime(last_modified, '%Y-%m-%d %H:%M:%S')
                        last_modified_date = last_modified_date.replace(tzinfo=timezone(timedelta(hours=3)))
                        if is_hours:
                            delta = timedelta(hours=time_ago)
                        else:
                            delta = timedelta(days=30 * time_ago)
                        if (last_modified_date + delta) <= current_time:
                            is_closed = ticket.close_date
                            if is_hours and (not is_closed or is_closed == 'None'):
                                result.append(ticket)
                            elif not is_hours:
                                result.append(ticket)

                    database_logger.info(f'Fetched all tickets modified before {time_ago} hours/month from database')
                    return result
                else:
                    database_logger.info('No TicketModels in a database')
                    return None

        async def delete(self, ticket: TicketModel):
            with self.session_maker() as session:
                destination = cf.project['storage'] + f'/{ticket.id}'
                if os.path.exists(destination):
                    shutil.rmtree(destination)
            session.query(TicketModel).filter_by(id=ticket.id).delete()
            database_logger.warning(f'TicketModel {ticket.id} is deleted!')
            session.commit()
            session.close()

        async def update(self, ticket: TicketModel):
            with self.session_maker() as session:
                session.query(TicketModel).filter_by(id=ticket.id).update({
                    'user_id': ticket.user_id,
                    'manager_id': ticket.manager_id,
                    'username': ticket.username,
                    'tg_name': ticket.tg_name,
                    'open_date': ticket.open_date,
                    'close_date': ticket.close_date,
                    'last_modified': ticket.last_modified,
                    'title': ticket.title,
                    'description': ticket.description,
                    'comment': ticket.comment,
                    'content': ticket.content
                })
                database_logger.warning(f'TicketModel {ticket.id} is updated!')
                session.commit()
                session.close()

    class Preference:
        def __init__(self, session_maker):
            self.session_maker = session_maker

        async def insert(self, preference: PreferenceModel):
            with self.session_maker() as session:
                session.add(preference)
                session.commit()
                database_logger.info(f'PreferenceModel is created!')
                session.close()

        async def get_all(self) -> list[PreferenceModel] | None:
            with self.session_maker() as session:
                data = session.query(PreferenceModel).all()
                if data:
                    database_logger.info('Fetched all PreferenceModels')
                    return data
                else:
                    database_logger.info('No PreferenceModels in a database')
                    return None

        async def get_by_key(self, key: str) -> PreferenceModel | None:
            with self.session_maker() as session:
                data = session.query(PreferenceModel).filter_by(key=key).first()
                if data:
                    database_logger.info(f'PreferenceModel {key} is retrieved from database')
                    session.close()
                    return data
                else:
                    database_logger.info(f'PreferenceModel {key} is not in database')
                    session.close()
                    return None

        async def delete(self, preference: PreferenceModel):
            with self.session_maker() as session:
                session.query(PreferenceModel).filter_by(key=preference.key).delete()
                database_logger.warning(f'PreferenceModel {preference.key} is deleted!')
                session.commit()
                session.close()

        async def update(self, preference: PreferenceModel):
            with self.session_maker() as session:
                session.query(PreferenceModel).filter_by(key=preference.key).update({
                    'key': preference.key,
                    'value': preference.value
                })
                database_logger.warning(f'PreferenceModel {preference.key} is updated!')
                session.commit()
                session.close()


db = Database(type_=Type.POSTGRESQL)


async def generate_start_data():
    from translations import strs
    faq = PreferenceModel()
    faq.key = 'faq'
    faq.value = {'questions': []}

    channel_info = PreferenceModel()
    channel_info.key = 'channel_info'
    channel_info.value = {
        'id': cf.DEFAULT_CHANNEL_ID,
        'url': cf.DEFAULT_CHANNEL_URL,
        'is_on': True,
        'button_name': 'Ссылка'
    }

    start_info = PreferenceModel()
    start_info.key = 'start_message'
    start_info.value = {'message': strs(lang='ru').general_start}

    auto_release = PreferenceModel()
    auto_release.key = 'release_hours'
    auto_release.value = {'hours': 1}

    auto_close = PreferenceModel()
    auto_close.key = 'close_hours'
    auto_close.value = {'hours': 36}

    faq_data = await db.preferences.get_by_key(key='faq')
    if not faq_data:
        await db.preferences.insert(preference=faq)

    channel_data = await db.preferences.get_by_key(key='channel_info')
    if not channel_data:
        await db.preferences.insert(preference=channel_info)

    start_data = await db.preferences.get_by_key(key='start_message')
    if not start_data:
        await db.preferences.insert(preference=start_info)

    release_info = await db.preferences.get_by_key(key='release_hours')
    if not release_info:
        await db.preferences.insert(preference=auto_release)

    close_data = await db.preferences.get_by_key(key='close_hours')
    if not close_data:
        await db.preferences.insert(preference=auto_close)
