# Standard
from datetime import datetime, timezone, timedelta

# Project
from database import db
from logger import background_logger
from bot import bot
from translations import strs


async def release_check():
    background_logger.warning('Starting one than one hour last modified tickets check')
    release = await db.preferences.get_by_key('release_hours')
    hours_ago = int(release.value.hours)
    more_than_hours_tickets = await db.tickets.get_tickets_last_modified_ago(hours_ago=hours_ago)
    if more_than_hours_tickets:
        for ticket in more_than_hours_tickets:
            ticket_manager_id = ticket.manager_id
            if not ticket_manager_id or ticket_manager_id == 'None':
                continue

            ticket.manager_id = None
            await db.tickets.update(ticket=ticket)

            manager = await db.users.get_by_id(user_id=ticket_manager_id)
            manager.current_ticket_id = None
            await db.user.update(user=manager)

            managers = await db.users.get_all_managers()
            if managers:
                user = await db.users.get_by_id(user_id=ticket.user_id)
                name, title, description = ticket.username, ticket.title, ticket.description
                tg_id, tg_name = user.id, user.tg_name
                ticket_info = strs(lang=user.lang).ticket_info(
                    id_=tg_id, tg_name=tg_name,
                    name=name, title=title, description=description
                )
                for manager in managers:
                    from ..private.managers.tickets import get_accept_ticket_inline_keyboard
                    if manager.id != ticket_manager_id:
                        await bot.send_message(
                            chat_id=manager.id,
                            text=strs(lang=manager.lang).ticket_not_updating_msg + ticket_info,
                            reply_markup=await get_accept_ticket_inline_keyboard(
                                ticket_id=ticket.id, lang=manager.lang
                            )
                        )
                    else:
                        await bot.send_message(
                            chat_id=manager.id,
                            text=strs(lang=user.lang).last_modified_manager_disconnected(time=hours_ago),
                        )


async def close_check():
    background_logger.warning('Starting one than thirty six hours last modified tickets check')
    close = await db.preferences.get_by_key('close_hours')
    hours_ago = int(close.value.get('hours'))
    more_than_hours_tickets = await db.tickets.get_tickets_last_modified_ago(hours_ago=hours_ago)
    if more_than_hours_tickets:
        current_date = datetime.now(timezone(timedelta(hours=3))) + timedelta(hours=3)
        for ticket in more_than_hours_tickets:
            ticket.close_date = current_date
            ticket.last_modified = current_date
            await db.tickets.update(ticket=ticket)

            ticket_manager_id = ticket.manager_id
            if ticket_manager_id:
                manager = await db.users.get_by_id(user_id=ticket_manager_id)
                manager.current_ticket_id = None
                await db.users.update(ticket=ticket)

                await bot.send_message(
                    chat_id=ticket_manager_id,
                    text=strs(lang=manager.lang).last_modified_outdated(time=hours_ago)
                )

            user_id = ticket.user_id
            user = await db.users.get_by_id(user_id=user_id)
            user.current_ticket_id = None
            await db.users.update(user=user)

            await bot.send_message(
                chat_id=user_id,
                text=strs(lang=user.lang).last_modified_outdated(time=hours_ago)
            )
