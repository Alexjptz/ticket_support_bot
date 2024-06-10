# Third-party
from aiogram.types import Message

# Standard
from datetime import datetime
from json import JSONEncoder, loads
from database import db, UserModel, TicketModel
import os

# Project
import config as cf
from translations import strs

BATCH = 3


# Custom JSON Encoder that handles datetime objects
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return JSONEncoder.default(self, obj)


async def make_up_ticket_page_text(lang: str, page: int, content, ticket: TicketModel, extended_info: bool = False) -> str:
    if content is str:
        content = content.replace('\'', '"').replace('None', 'null').replace('True', 'true').replace('False', 'false')
        content = loads(content)
    upper = page * BATCH if len(content) > page * BATCH else len(content)
    lower = upper - BATCH if upper - BATCH >= 0 else 0
    message_text = strs(lang=lang).history_ticket(ticket.id, upper, len(content))
    for i in range(lower, upper):
        message_info = content[i]
        message = Message(**message_info)
        media_group_id = message.media_group_id
        media_group_text = media_group_id
        user_id = message.chat.id
        manager_id = ticket.manager_id
        text = message.html_text
        msg_caption = message.caption
        is_manager = manager_id == user_id if manager_id else False

        message_id = message.message_id

        manager_info = user_info = None
        if extended_info:
            if is_manager:
                manager_id = ticket.manager_id
                manager_info = strs(lang=lang).manager_extended(manager_id, message_id, media_group_text)
            else:
                user_id = ticket.user_id
                user_info = strs(lang=lang).user_extended(user_id, message_id, media_group_text)
        else:
            if is_manager:
                manager_info = strs(lang=lang).manager_usual(message_id, media_group_text)
            else:
                user_info = strs(lang=lang).user_usual(message_id, media_group_text)

        if is_manager:
            message_text += manager_info
        else:
            message_text += user_info

        if text:
            if msg_caption:
                message_text += strs(lang=lang).media_files_in_msg
            message_text += text + '\n____________________________________\n\n'
        else:
            message_text += strs(lang=lang).media_files_in_msg
            message_text += '____________________________________\n\n'

    return message_text


async def get_media_messages(lang: str, page: int, ticket: TicketModel) -> list[Message]:
    content = ticket.content
    if content is str:
        content = content.replace('\'', '"').replace('None', 'null').replace('True', 'true').replace('False', 'false')
        content = loads(content)

    upper = page * BATCH if len(content) > page * BATCH else len(content)
    lower = upper - BATCH if upper - BATCH >= 0 else 0

    messages = []
    for i in range(lower, upper):
        msg_info = content[i]
        message = Message(**msg_info)
        message_id = message.message_id
        media_group_id = message.media_group_id
        media_group_text = media_group_id

        path = f'{cf.project["storage"]}/{ticket.id}/media_info.txt'
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-16') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith(f'{message_id} {media_group_id}'):
                        message = Message(**msg_info)
                        caption = message.html_text
                        if caption:
                            caption = strs(lang=lang).msg_caption(message_id, media_group_text) + caption
                        else:
                            caption = strs(lang=lang).msg_caption(message_id, media_group_text)

                        msg_info = message.model_dump()
                        msg_info['caption'] = caption
                        messages.append(Message(**msg_info))

    return messages


async def make_up_tickets_info_page(lang: str, page: int, tickets: list[TicketModel], is_extended: bool = False):
    upper = page * BATCH if len(tickets) > page * BATCH else len(tickets)
    lower = upper - BATCH if upper - BATCH >= 0 else 0

    tickets_info = strs(lang=lang).conversations(upper, len(tickets))
    for i in range(lower, upper):
        ticket = tickets[i]
        ticket_id = ticket.id
        opened = str(ticket.open_date).split('.')[0]
        closed = str(ticket.close_date).split('.')[0]
        comment = ticket.comment
        name, title, description = ticket.username, ticket.title, ticket.description
        tg_name = ticket.tg_name

        user = await db.users.get_by_id(user_id=ticket.user_id)
        tickets_info += strs(lang=lang).tickets_info(is_extended=is_extended).format(
            ticket_id, opened, closed, name, tg_name, user.url_name, title, description, comment
        )

    return tickets_info


async def make_up_user_info(lang: str, user: UserModel) -> tuple:
    tg_name, tg_id, status = user.tg_name, int(user.id), user.status
    mute_time, is_banned = str(user.mute_time), user.is_banned
    url_name = user.url_name
    as_user_tickets = await db.tickets.get_all_by_id(user_id=tg_id, is_manager=False)
    as_manager_tickets = await db.tickets.get_all_by_id(user_id=tg_id, is_manager=True)

    is_manager = False

    status_text = ''
    match status:
        case 'user':
            status_text = strs(lang=lang).status_usual
        case 'manager':
            is_manager = True
            status_text = strs(lang=lang).status_manager
        case 'admin':
            is_manager = True
            status_text = strs(lang=lang).status_admin

    text = strs(lang=lang).user_info.format(
        tg_name, tg_id, url_name, status_text,
        0 if not as_user_tickets else len(as_user_tickets),
        0 if not as_manager_tickets else len(as_manager_tickets)
    )
    if is_banned:
        text += strs(lang=lang).user_is_banned(is_banned)
    else:
        text += strs(lang=lang).user_restricted.format(mute_time.split(".")[0] if (mute_time and mute_time != "None") else "None")
        text += strs(lang=lang).user_is_banned(False)

    return is_manager, text
