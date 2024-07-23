# Third-party
import sqlalchemy.exc
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

# Standard
import os
import shutil
import traceback
from datetime import datetime, timedelta, timezone
from enum import Enum
from time import sleep

# Project
import config as cf
from logger import database_logger
from translations import strs

from .models import (CategoryModel, PreferenceModel, QuestionModel,
                     TicketModel, UserModel, base)


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
                self.preferences = self.Preference(
                    session_maker=self.session_maker
                    )
                self.categories = self.Category(
                    session_maker=self.session_maker
                    )
                self.questions = self.Question(
                    session_maker=self.session_maker
                )

                database_logger.info('Connected to database')
                break
            except sqlalchemy.exc.OperationalError:
                # Handling database connection errors
                database_logger.error(
                    'Database error:\n' + traceback.format_exc()
                    )
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
                database_logger.info(
                    'UserModel is created!'
                    )
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
                data = session.query(UserModel).filter(
                    UserModel.mute_time.isnot(None)
                    ).all()
                if data:
                    database_logger.info('Fetched all muted UserModels')
                    return data
                else:
                    database_logger.info('No muted UserModels in a database')
                    return None

        async def get_all_managers(self) -> list[UserModel] | None:
            with self.session_maker() as session:
                data = session.query(UserModel).filter_by(
                    status='manager'
                    ).all()
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
                    database_logger.info(
                        f'UserModel {user_id} is retrieved from database'
                        )
                    session.close()
                    return data
                else:
                    database_logger.info(
                        f'UserModel {user_id} is not in database'
                        )
                    session.close()
                    return None

        async def get_by_tg_name(self, tg_name: str) -> UserModel | None:
            with self.session_maker() as session:
                data = session.query(UserModel).filter_by(
                    tg_name=tg_name
                    ).first()
                if data:
                    database_logger.info(
                        f'UserModel {tg_name} is retrieved from database'
                        )
                    session.close()
                    return data
                else:
                    database_logger.info(
                        f'UserModel {tg_name} is not in database'
                        )
                    session.close()
                    return None

        async def get_by_url_name(self, url_name: str) -> UserModel | None:
            with self.session_maker() as session:
                data = session.query(UserModel).filter_by(
                    url_name=url_name
                    ).first()
                if data:
                    database_logger.info(
                        f'UserModel {url_name} is retrieved from database'
                        )
                    session.close()
                    return data
                else:
                    database_logger.info(
                        f'UserModel {url_name} is not in database'
                        )
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
                database_logger.info('TicketModel is created!')
                session.close()
                return ticket_id

        async def get_all(self) -> list[TicketModel] | None:
            with self.session_maker() as session:
                data = session.query(TicketModel).order_by(
                    desc(TicketModel.id)
                    ).all()
                if data:
                    database_logger.info('Fetched all TicketModels')
                    return data
                else:
                    database_logger.info('No TicketModels in a database')
                    return None

        async def get_by_id(self, ticket_id: str | int) -> TicketModel | None:
            with self.session_maker() as session:
                data = session.query(TicketModel).filter_by(
                    id=int(ticket_id)
                    ).first()
                if data:
                    database_logger.info(
                        f'TicketModel {ticket_id} is retrieved from database'
                        )
                    session.close()
                    return data
                else:
                    database_logger.info(
                        f'TicketModel {ticket_id} is not in database'
                        )
                    session.close()
                    return None

        async def get_all_opened(self) -> list[TicketModel] | None:
            with self.session_maker() as session:
                data = session.query(TicketModel).filter_by(
                    close_date=None, manager_id=None
                    ).order_by(desc(TicketModel.id)).all()
                if data:
                    database_logger.info(
                        'Fetched all opened TicketModels'
                        )
                    return data
                else:
                    database_logger.info(
                        'No opened TicketModels in a database'
                        )
                    return None

        async def get_all_by_id(
            self, user_id: int, is_manager: bool
            ) -> list[TicketModel] | None:
            with self.session_maker() as session:
                if is_manager:
                    data = session.query(TicketModel).filter_by(
                        manager_id=user_id
                        ).order_by(desc(TicketModel.id)).all()
                else:
                    data = session.query(TicketModel).filter_by(
                        user_id=user_id
                        ).order_by(desc(TicketModel.id)).all()
                if data:
                    database_logger.info(
                        f'Fetched all TicketModels with user/manager id {user_id}'
                        )
                    return data
                else:
                    database_logger.info(
                        f'No TicketModels in a database with user/manager id {user_id}'
                        )
                    return None

        async def get_tickets_last_modified_ago(
            self, time_ago: int, is_hours=True
            ) -> list[TicketModel] | None:
            with self.session_maker() as session:
                data = session.query(TicketModel).filter_by(
                    close_date=None, manager_id=None
                    ).all()
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

                    database_logger.info(
                        f'Fetched all tickets modified before {time_ago} hours/month from database'
                        )
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
                    'manager_username': ticket.manager_username,
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
                database_logger.info('PreferenceModel is created!')
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
                data = session.query(PreferenceModel).filter_by(
                    key=key
                    ).first()
                if data:
                    database_logger.info(
                        f'PreferenceModel {key} is retrieved from database'
                        )
                    session.close()
                    return data
                else:
                    database_logger.info(
                        f'PreferenceModel {key} is not in database'
                        )
                    session.close()
                    return None

        async def delete(self, preference: PreferenceModel):
            with self.session_maker() as session:
                session.query(PreferenceModel).filter_by(
                    key=preference.key
                    ).delete()
                database_logger.warning(
                    f'PreferenceModel {preference.key} is deleted!'
                    )
                session.commit()
                session.close()

        async def update(self, preference: PreferenceModel):
            with self.session_maker() as session:
                session.query(PreferenceModel).filter_by(
                    key=preference.key
                    ).update({
                    'key': preference.key,
                    'value': preference.value
                })
                database_logger.warning(
                    f'PreferenceModel {preference.key} is updated!'
                    )
                session.commit()
                session.close()

    class Category:
        def __init__(self, session_maker):
            self.session_maker = session_maker

        async def insert(self, category: CategoryModel):
            with self.session_maker() as session:
                session.add(category)
                session.commit()
                category_id = category.id
                database_logger.info('CategoryModel is created!')
                session.close()
                return category_id

        async def get_all(self) -> list[CategoryModel] | None:
            with self.session_maker() as session:
                data = session.query(CategoryModel).order_by(
                    desc(CategoryModel.id)
                    ).all()
                if data:
                    database_logger.info('Fetched all CategoryModel')
                    return data
                else:
                    database_logger.info('No CateegoryModels in a database')
                    return None

        async def get_by_name(
            self, category_name: str | int
            ) -> CategoryModel | None:
            with self.session_maker() as session:
                data = session.query(CategoryModel).filter_by(
                    name=str(category_name)
                    ).first()
                if data:
                    database_logger.info(
                        f'Category {category_name} is retrivied from database'
                        )
                    session.close()
                    return data
                else:
                    database_logger.info(
                        f'CategoryModel {category_name} is not in database'
                        )
                    session.close()
                    return None

        async def get_by_id(
            self, category_id: str | int
            ) -> CategoryModel | None:
            with self.session_maker() as session:
                data = session.query(CategoryModel).filter_by(
                    id=int(category_id)
                    ).first()
                if data:
                    database_logger.info(
                        f'Category {category_id} is retrieved from database'
                        )
                    session.close()
                    return data
                else:
                    database_logger.info(
                        f'CategoryModel {category_id} is not in database'
                        )
                    session.close()
                    return None

        async def delete(self, category_id: int | str):
            with self.session_maker() as session:
                session.query(CategoryModel).filter_by(
                    id=category_id
                    ).delete()
                database_logger.warning(
                    f'CategoryModel {category_id} is deleted!'
                    )
                session.commit()
                session.close()

        async def update(self, category_id: int, update_data: dict):
            with self.session_maker() as session:
                session.execute(
                    update(CategoryModel).where(
                        CategoryModel.id == category_id
                    ).values(update_data)
                )
                database_logger.warning(
                    f'CategoryModel {category_id} is updated with {update_data}'
                )
                session.commit()
                session.close()

    class Question:
        def __init__(self, session_maker):
            self.session_maker = session_maker

        async def insert(self, question: QuestionModel):
            with self.session_maker() as session:
                session.add(question)
                session.commit()
                question_id = question.id
                database_logger.info(
                    f'QuestionModel is created!'
                    )
                session.close()
                return question_id

        async def get_all(self) -> list[QuestionModel] | None:
            with self.session_maker() as session:
                data = session.query(QuestionModel).order_by(
                    desc(QuestionModel.id)
                    ).all()
                if data:
                    database_logger.info('Fetched all QuestionModel')
                    return data
                else:
                    database_logger.info('No QuestionModels in a database')
                    return None

        async def get_all_by_id(
            self, category_id: str | int
        ) -> QuestionModel | None:
            with self.session_maker() as session:
                questions = session.query(QuestionModel).filter_by(
                category_id=category_id
                ).all()
                if questions:
                    database_logger.info(
                        f'Questions by {category_id} are retrieved from database'
                    )
                    session.close()
                    return questions
                else:
                    database_logger.info(
                        f'No questions by category {category_id} in database'
                    )
                    session.close()
                    return None

        async def get_by_id(
            self, question_id: str | int
            ) -> QuestionModel | None:
            with self.session_maker() as session:
                data = session.query(QuestionModel).filter_by(
                    id=int(question_id)
                    ).first()
                if data:
                    database_logger.info(
                        f'Question {question_id} is retrieved from database'
                        )
                    session.close()
                    return data
                else:
                    database_logger.info(
                        f'QuestionModel {question_id} is not in database'
                        )
                    session.close()
                    return None

        async def delete(self, question: QuestionModel):
            with self.session_maker() as session:
                session.query(QuestionModel).filter_by(
                    id=question.id
                    ).delete()
                database_logger.warning(
                    f'QuestionModel {question.id} is deleted!'
                    )
                session.commit()
                session.close()

        async def update(self, question_id: int, update_data: dict):
            with self.session_maker() as session:
                session.execute(
                    update(QuestionModel).where(
                        QuestionModel.id == question_id
                    ).values(update_data)
                )
                database_logger.warning(
                    f'QuestionModel {question_id} is updated with {update_data}'
                )
                session.commit()
                session.close()


db = Database(type_=Type.POSTGRESQL)


"""Generate data for the first initiation of database"""
async def generate_start_data():

    check_categories = await db.categories.get_all()
    if not check_categories:
        for category_id in range(1, 4):
            category_name = f'Категория {category_id}'
            category_description = (
                f'Описание {category_id}'
                )
            new_category = CategoryModel(
                name=category_name,
                description=category_description,
            )
            new_category_id = await db.categories.insert(new_category)
            for q in range(1, 3):
                question_name = f'Вопрос {q}'
                question_answer = (
                    f'Ответ на вопрос {q} в категории {category_id}'
                    )
                new_question = QuestionModel(
                    category_id=new_category_id,
                    name=question_name,
                    answer=question_answer,
                )
                await db.questions.insert(new_question)

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
