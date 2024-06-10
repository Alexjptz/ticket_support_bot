# Third-party
from sqladmin import ModelView

# Project
from database import UserModel, TicketModel, PreferenceModel


class UserView(ModelView, model=UserModel):
    name = 'Пользователь'
    name_plural = 'Пользователи'
    column_labels = {
        UserModel.id: 'ID пользователя',
        UserModel.tg_name: 'Telegram имя',
        UserModel.url_name: 'URL имя',
        UserModel.status: 'Статус',
        UserModel.lang: 'Язык',
        UserModel.current_ticket_id: 'ID текущего тикета',
        UserModel.mute_time: 'Ограничен до',
        UserModel.is_banned: 'Заблокирован?',
    }
    column_list = [
        UserModel.id,
        UserModel.tg_name,
        UserModel.url_name,
        UserModel.status,
        UserModel.lang,
        UserModel.current_ticket_id,
        UserModel.mute_time,
        UserModel.is_banned,
    ]
    column_sortable_list = column_list
    column_searchable_list = [
        UserModel.id,
        UserModel.tg_name,
        UserModel.url_name,
        UserModel.status,
    ]


class TicketView(ModelView, model=TicketModel):
    name = 'Тикет'
    name_plural = 'Тикеты'
    column_labels = {
        TicketModel.id: 'ID тикета',
        TicketModel.user_id: 'ID пользователя',
        TicketModel.manager_id: 'ID менеджера',
        TicketModel.username: 'Имя пользователя',
        TicketModel.tg_name: 'Telegram имя',
        TicketModel.open_date: 'Дата открытия',
        TicketModel.last_modified: 'Дата последнего изменения',
        TicketModel.close_date: 'Дата закрытия',
        TicketModel.title: 'Заголовок',
        TicketModel.description: 'Описание',
        TicketModel.comment: 'Комментарий',
        TicketModel.content: 'Содержание',
    }
    column_list = [
        TicketModel.id,
        TicketModel.user_id,
        TicketModel.manager_id,
        TicketModel.username,
        TicketModel.tg_name,
        TicketModel.open_date,
        TicketModel.last_modified,
        TicketModel.close_date,
        TicketModel.title,
        TicketModel.comment,
        TicketModel.description,
    ]
    column_sortable_list = column_list
    column_searchable_list = [
        TicketModel.id,
        TicketModel.user_id,
        TicketModel.username,
        TicketModel.tg_name,
    ]


class PreferenceView(ModelView, model=PreferenceModel):
    name = 'Настройка'
    name_plural = 'Настройки'
    column_labels = {
        PreferenceModel.key: 'Ключ',
        PreferenceModel.value: 'Значение',
    }
    column_list = [
        PreferenceModel.key,
        PreferenceModel.value,
    ]
    column_sortable_list = column_list
    column_searchable_list = [
        PreferenceModel.key,
    ]
