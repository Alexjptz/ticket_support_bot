from . import *

# Standard
from datetime import datetime, timezone, timedelta
from json import dumps, loads
import os

# Project
from handlers.utils import BATCH, get_media_messages, make_up_ticket_page_text, make_up_tickets_info_page

# __router__ !DO NOT DELETE!
ticket_router = Router()


# __states__ !DO NOT DELETE!
class CreateTicketStates(StatesGroup):
    get_name = State()
    get_title = State()
    get_description = State()


# __buttons__ !DO NOT DELETE!
async def get_media_menu_inline_keyboard(lang: str, ticket_page: int, ticket_id: str,
                                         page: int) -> InlineKeyboardMarkup:
    button_list = [
        [InlineKeyboardButton(text='⏪', callback_data=f'media_prev_btn {ticket_id} {ticket_page} {page}'),
         InlineKeyboardButton(text='⏩', callback_data=f'media_next_btn {ticket_id} {ticket_page} {page}')],
        [InlineKeyboardButton(text=strs(lang=lang).delete_btn, callback_data='media_close_btn')],
    ]

    @ticket_router.callback_query(F.data.startswith('media_prev_btn'), filters.IsUser())
    async def handle_media_prev_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling media_menu media_prev button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        ticket_id, ticket_page, page = data[1], int(data[2]), int(data[3])

        ticket = await db.tickets.get_by_id(ticket_id=ticket_id)
        messages = await get_media_messages(lang=(await state.get_data())['lang'], page=ticket_page, ticket=ticket)

        prev_page = page
        page = page - 1 if page != 1 else len(messages)
        if page != prev_page:
            current_message = messages[page - 1]
            await callback.message.delete()
            await current_message.send_copy(
                chat_id=callback.message.chat.id,
                reply_markup=await get_media_menu_inline_keyboard(
                    ticket_page=ticket_page, ticket_id=ticket_id, page=page, lang=(await state.get_data())['lang']
                ),
                parse_mode='html'
            ).as_(callback.bot)

        await callback.answer()

    @ticket_router.callback_query(F.data.startswith('media_next_btn'), filters.IsUser())
    async def handle_media_next_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling media_menu media_next button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        ticket_id, ticket_page, page = data[1], int(data[2]), int(data[3])

        ticket = await db.tickets.get_by_id(ticket_id=ticket_id)
        messages = await get_media_messages(page=ticket_page, ticket=ticket, lang=(await state.get_data())['lang'])

        prev_page = page
        page = page + 1 if page != len(messages) else 1
        if page != prev_page:
            current_message = messages[page - 1]
            await callback.message.delete()
            await current_message.send_copy(
                chat_id=callback.message.chat.id,
                reply_markup=await get_media_menu_inline_keyboard(
                    ticket_page=ticket_page, ticket_id=ticket_id, page=page, lang=(await state.get_data())['lang']
                ),
                parse_mode='html'
            ).as_(callback.bot)

        await callback.answer()

    @ticket_router.callback_query(F.data.startswith('media_close_btn'), filters.IsUser())
    async def handle_media_close_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling media_menu media_close button callback from user {callback.message.chat.id}')
        await callback.message.delete()
        await callback.answer()

    return InlineKeyboardMarkup(inline_keyboard=button_list)


async def get_archive_menu_inline_keyboard(lang: str, tickets: list[TicketModel], page: int) -> InlineKeyboardMarkup:
    button_list = []

    from math import ceil
    max_pages = ceil(len(tickets) / BATCH)

    upper = page * BATCH if len(tickets) > page * BATCH else len(tickets)
    lower = upper - BATCH if upper - BATCH >= 0 else 0
    if tickets:
        for i in range(lower, upper):
            ticket = tickets[i]
            ticket_id = ticket.id
            button_list.append(
                [InlineKeyboardButton(text=f'Тикет {ticket_id}',
                                      callback_data=f'archive_ticket_btn {ticket_id} {page}')])

    button_list.append(
        [InlineKeyboardButton(text='⏪', callback_data=f'archive_prev_btn {page} {max_pages}'),
         InlineKeyboardButton(text='⏩', callback_data=f'archive_next_btn {page} {max_pages}')]
    )
    button_list.append(
        [InlineKeyboardButton(text=strs(lang=lang).back_btn, callback_data='archive_back_btn')]
    )

    @ticket_router.callback_query(F.data.startswith('archive_ticket_btn'), filters.IsUser())
    async def handle_ticket_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling archive_menu ticket button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        ticket_id, page = data[1], int(data[2])

        ticket = await db.tickets.get_by_id(ticket_id=ticket_id)
        content = ticket.content

        ticket_text = await make_up_ticket_page_text(page=1, content=content, ticket=ticket,
                                                     lang=(await state.get_data())['lang'])
        await callback.message.edit_text(
            text=ticket_text,
            reply_markup=await get_ticket_history_inline_keyboard(
                ticket_id=ticket_id, page=1, back_data=f'history_back_l_btn {page}',
                lang=(await state.get_data())['lang']
            )
        )

        await callback.answer()

    @ticket_router.callback_query(F.data.startswith('archive_prev_btn'), filters.IsUser())
    async def handle_prev_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling archive_menu prev button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        page, max_pages = int(data[1]), int(data[2])

        prev_page = page
        page = page - 1 if page != 1 else max_pages

        tickets = await db.tickets.get_all_by_id(user_id=callback.message.chat.id, is_manager=False)
        text = await make_up_tickets_info_page(lang=(await state.get_data())['lang'], page=page, tickets=tickets)
        if prev_page != page:
            await callback.message.edit_text(
                text=text,
                reply_markup=await get_archive_menu_inline_keyboard(
                    tickets=tickets,
                    page=page, lang=(await state.get_data())['lang']
                )
            )
        await callback.answer()

    @ticket_router.callback_query(F.data.startswith('archive_next_btn'), filters.IsUser())
    async def handle_next_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling archive_menu next button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        page, max_pages = int(data[1]), int(data[2])

        prev_page = page
        page = page + 1 if page != max_pages else 1

        tickets = await db.tickets.get_all_by_id(user_id=callback.message.chat.id, is_manager=False)
        text = await make_up_tickets_info_page(lang=(await state.get_data())['lang'], page=page, tickets=tickets)
        if prev_page != page:
            await callback.message.edit_text(
                text=text,
                reply_markup=await get_archive_menu_inline_keyboard(
                    tickets=tickets,
                    page=page, lang=(await state.get_data())['lang']
                )
            )
        await callback.answer()

    @ticket_router.callback_query(F.data.startswith('archive_back_btn'), filters.IsUser())
    async def handle_back_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling archive_menu back button callback from user {callback.message.chat.id}')

        user = await db.users.get_by_id(user_id=callback.message.chat.id)
        current_ticket_id = user.current_ticket_id

        ticket = None
        ticket_info = strs(lang=(await state.get_data())['lang']).ticket_no_opened
        if current_ticket_id:
            ticket = await db.tickets.get_by_id(ticket_id=current_ticket_id)
            if ticket:
                name, title, description = ticket.username, ticket.title, ticket.description
                tg_id, tg_name = user.id, user.tg_name
                ticket_info = strs(lang=(await state.get_data())['lang']).ticket_info(
                    id_=tg_id, tg_name=tg_name,
                    name=name, title=title, description=description
                )

        ticket_id = None if not ticket else ticket.id
        is_current = True if current_ticket_id else False
        await callback.message.edit_text(
            text=ticket_info,
            reply_markup=await get_ticket_menu_inline_keyboard(
                ticket_id=ticket_id, is_current=is_current, lang=(await state.get_data())['lang']
            )
        )
        await callback.answer()

    return InlineKeyboardMarkup(inline_keyboard=button_list)


async def get_ticket_history_inline_keyboard(
        lang: str, ticket_id: str, page: int, back_data: str = 'history_back_my_btn'
) -> InlineKeyboardMarkup:
    button_list = [
        [InlineKeyboardButton(text='⏪', callback_data=f'history_prev_btn {ticket_id} {page}'),
         InlineKeyboardButton(text='📥', callback_data=f'history_open_media_btn {ticket_id} {page}'),
         InlineKeyboardButton(text='⏩', callback_data=f'history_next_btn {ticket_id} {page}')],
        [InlineKeyboardButton(text=strs(lang=lang).back_btn, callback_data=f'{back_data}')],
    ]

    @ticket_router.callback_query(F.data.startswith('history_prev_btn'), filters.IsUser())
    async def handle_prev_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling ticket_history prev button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        ticket_id, page = data[1], int(data[2])

        ticket = await db.tickets.get_by_id(ticket_id=ticket_id)
        content = ticket.content
        content = [] if not content else content

        prev_page = page
        from math import ceil
        max_pages = ceil(len(content) / BATCH)
        page = page - 1 if page != 1 else max_pages

        user = await db.users.get_by_id(user_id=callback.message.chat.id)
        current_ticket_id = user.current_ticket_id
        back_data = 'history_back_l_btn 1'
        if current_ticket_id:
            back_data = 'history_back_my_btn'

        if prev_page != page:
            ticket_text = await make_up_ticket_page_text(page=page, content=content, ticket=ticket,
                                                         lang=(await state.get_data())['lang'])
            await callback.message.edit_text(
                text=ticket_text,
                reply_markup=await get_ticket_history_inline_keyboard(
                    ticket_id=ticket_id,
                    page=page,
                    back_data=back_data,
                    lang=(await state.get_data())['lang']
                )
            )
        await callback.answer()

    @ticket_router.callback_query(F.data.startswith('history_next_btn'), filters.IsUser())
    async def handle_next_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling ticket_history next button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        ticket_id, page = data[1], int(data[2])

        ticket = await db.tickets.get_by_id(ticket_id=ticket_id)
        content = ticket.content
        content = [] if not content else content

        from math import ceil
        max_pages = ceil(len(content) / BATCH)
        prev_page = page
        page = page + 1 if page != max_pages else 1

        user = await db.users.get_by_id(user_id=callback.message.chat.id)
        current_ticket_id = user.current_ticket_id
        back_data = 'history_back_l_btn 1'
        if current_ticket_id:
            back_data = 'history_back_my_btn'

        if prev_page != page:
            ticket_text = await make_up_ticket_page_text(page=page, content=content, ticket=ticket,
                                                         lang=(await state.get_data())['lang'])
            await callback.message.edit_text(
                text=ticket_text,
                reply_markup=await get_ticket_history_inline_keyboard(
                    ticket_id=ticket_id,
                    page=page,
                    back_data=back_data,
                    lang=(await state.get_data())['lang']
                )
            )
        await callback.answer()

    @ticket_router.callback_query(F.data.startswith('history_open_media_btn'), filters.IsUser())
    async def handle_open_media_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling ticket_history open_media button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        ticket_id, page = data[1], int(data[2])

        ticket = await db.tickets.get_by_id(ticket_id=ticket_id)
        messages = await get_media_messages(page=page, ticket=ticket, lang=(await state.get_data())['lang'])
        if messages:
            current_message = messages[0]
            await current_message.send_copy(
                chat_id=callback.message.chat.id,
                reply_markup=await get_media_menu_inline_keyboard(
                    ticket_page=page, ticket_id=ticket_id, page=1, lang=(await state.get_data())['lang']
                ),
                parse_mode='html'
            ).as_(callback.bot)
        else:
            await callback.answer(text=strs(lang=(await state.get_data())['lang']).ticket_no_media_on_page,
                                  show_alert=True)

        await callback.answer()

    @ticket_router.callback_query(F.data.startswith('history_back_my_btn'), filters.IsUser())
    async def handle_back_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(
            f'Handling ticket_history back to my tickets menu button callback from user {callback.message.chat.id}')

        user = await db.users.get_by_id(user_id=callback.message.chat.id)
        current_ticket_id = user.current_ticket_id

        text = strs(lang=(await state.get_data())['lang']).ticket_no_opened
        ticket = None
        is_current = False
        if current_ticket_id:
            is_current = True
            ticket = await db.tickets.get_by_id(ticket_id=current_ticket_id)
            name, title, description = ticket.username, ticket.title, ticket.description
            tg_id, tg_name = user.id, user.tg_name
            ticket_info = strs(lang=(await state.get_data())['lang']).ticket_info(
                id_=tg_id, tg_name=tg_name,
                name=name, title=title, description=description
            )
            text = strs(lang=(await state.get_data())['lang']).current_ticket_composition.format(ticket_info)

        await callback.message.edit_text(
            text=text,
            reply_markup=await get_ticket_menu_inline_keyboard(
                is_current=is_current,
                ticket_id=None if not ticket else ticket.id,
                lang=(await state.get_data())['lang']
            )
        )
        await callback.answer()

    @ticket_router.callback_query(F.data.startswith('history_back_l_btn'), filters.IsUser())
    async def handle_back_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling ticket_history back to list button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        page = int(data[1])

        tickets = await db.tickets.get_all_by_id(user_id=callback.message.chat.id, is_manager=False)
        text = await make_up_tickets_info_page(page=page, tickets=tickets, lang=(await state.get_data())['lang'])
        await callback.message.edit_text(
            text=text,
            reply_markup=await get_archive_menu_inline_keyboard(
                tickets=tickets,
                page=page,
                lang=(await state.get_data())['lang']
            )
        )

        await callback.answer()

    return InlineKeyboardMarkup(inline_keyboard=button_list)


async def get_ticket_menu_inline_keyboard(
        lang: str,
        ticket_id: str | None = None,
        is_current: bool = False
) -> InlineKeyboardMarkup:
    button_list = []
    if is_current:
        button_list = [
            [InlineKeyboardButton(text=strs(lang=lang).delete_btn, callback_data=f'close_btn {ticket_id}'),
             InlineKeyboardButton(text=strs(lang=lang).history_btn, callback_data=f'history_btn {ticket_id}')],
        ]
    button_list.append([InlineKeyboardButton(text=strs(lang=lang).archive_btn, callback_data='archive_btn')], )

    @ticket_router.callback_query(F.data.startswith('close_btn'), filters.IsUser())
    async def handle_close_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling ticket_menu close button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        ticket_id_ = data[1]
        ticket = await db.tickets.get_by_id(ticket_id=ticket_id_)
        if ticket:
            current_date = datetime.now(timezone(timedelta(hours=3))) + timedelta(hours=3)
            ticket.close_date = current_date
            ticket.last_modified = current_date
            await db.tickets.update(ticket=ticket)

            user = await db.users.get_by_id(user_id=callback.message.chat.id)
            user.current_ticket_id = None
            await db.users.update(user=user)

            manager_id = ticket.manager_id
            if manager_id:
                manager = await db.users.get_by_id(user_id=manager_id)
                ticket_info = strs(lang=manager.lang).ticket_closed_by_user(
                    name=ticket.username, title=ticket.title, description=ticket.description
                )
                await callback.bot.send_message(
                    chat_id=manager_id,
                    text=ticket_info
                )
                manager = await db.users.get_by_id(user_id=manager_id)
                manager.current_ticket_id = None
                await db.users.update(user=manager)

            await callback.message.edit_text(
                text=strs(lang=(await state.get_data())['lang']).ticket_no_opened,
                reply_markup=await get_ticket_menu_inline_keyboard(lang=(await state.get_data())['lang'],
                                                                   is_current=False)
            )
        await callback.answer()

    @ticket_router.callback_query(F.data.startswith('history_btn'), filters.IsUser())
    async def handle_history_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling ticket_menu history button callback from user {callback.message.chat.id}')
        user = await db.users.get_by_id(user_id=callback.message.chat.id)
        current_ticket = await db.tickets.get_by_id(ticket_id=user.current_ticket_id)
        content = current_ticket.content
        if content:
            ticket_text = await make_up_ticket_page_text(page=1, content=content, ticket=current_ticket,
                                                         lang=(await state.get_data())['lang'])
            await callback.message.edit_text(
                text=ticket_text,
                reply_markup=await get_ticket_history_inline_keyboard(
                    ticket_id=ticket_id,
                    page=1,
                    lang=(await state.get_data())['lang']
                )
            )
        else:
            await callback.message.answer(text=strs(lang=(await state.get_data())['lang']).ticket_no_history)
        await callback.answer()

    @ticket_router.callback_query(F.data.startswith('archive_btn'), filters.IsUser())
    async def handle_archive_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling ticket_menu archive button callback from user {callback.message.chat.id}')
        tickets = await db.tickets.get_all_by_id(user_id=callback.message.chat.id, is_manager=False)

        if tickets:
            text = await make_up_tickets_info_page(page=1, tickets=tickets, lang=(await state.get_data())['lang'])
            await callback.message.edit_text(
                text=text,
                reply_markup=await get_archive_menu_inline_keyboard(
                    tickets=tickets, page=1, lang=(await state.get_data())['lang']
                )
            )
        else:
            await callback.answer(text=strs(lang=(await state.get_data())['lang']).tickets_no_archive, show_alert=True)

        await callback.answer()

    return InlineKeyboardMarkup(inline_keyboard=button_list)


# __chat__ !DO NOT DELETE!
@ticket_router.message(
    filters.Private(), filters.IsUser(),
    ((F.text == '/create_ticket') | (F.text.in_(create_ticket_btn))),
    filters.IsRestricted(),
)
async def handle_create_ticket_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /create_ticket from user {message.chat.id}')
    user = await db.users.get_by_id(user_id=message.chat.id)
    current_ticket_id = user.current_ticket_id
    if not current_ticket_id:
        from . import get_decline_reply_keyboard
        await message.answer(text=strs(lang=(await state.get_data())['lang']).ticket_ask_name,
                             reply_markup=await get_decline_reply_keyboard(lang=(await state.get_data())['lang']))
        await state.set_state(CreateTicketStates.get_name.state)
        return
    await message.answer(text=strs(lang=(await state.get_data())['lang']).ticket_opened_already)


@ticket_router.message(CreateTicketStates.get_name)
async def handle_get_name_state(message: Message, state: FSMContext):
    bot_logger.info(f'Handling states CreateTicketStates.get_name from user {message.chat.id}')
    name = message.text
    if name and len(name) < 50:
        await message.answer(text=strs(lang=(await state.get_data())['lang']).ticket_ask_title)
        await state.update_data({'name': name})
        await state.set_state(CreateTicketStates.get_title.state)
    else:
        await message.answer(text=strs(lang=(await state.get_data())['lang']).ticket_ask_name_error)


@ticket_router.message(CreateTicketStates.get_title)
async def handle_get_title_state(message: Message, state: FSMContext):
    bot_logger.info(f'Handling states CreateTicketStates.get_title from user {message.chat.id}')
    title = message.text
    if title and len(title) < 50:
        await message.answer(text=strs(lang=(await state.get_data())['lang']).ticket_ask_description)
        await state.update_data({'title': title})
        await state.set_state(CreateTicketStates.get_description.state)
    else:
        await message.answer(text=strs(lang=(await state.get_data())['lang']).ticket_ask_title_error)


@ticket_router.message(CreateTicketStates.get_description)
async def handle_get_description_state(message: Message, state: FSMContext):
    bot_logger.info(f'Handling states CreateTicketStates.get_description from user {message.chat.id}')
    description = message.text
    if description and len(description) < 100:
        data = await state.get_data()
        name, title = data['name'], data['title']
        current_time = datetime.now(timezone(timedelta(hours=3))) + timedelta(hours=3)

        ticket = TicketModel()
        ticket.user_id = message.chat.id
        ticket.username = name
        ticket.tg_name = message.from_user.full_name
        ticket.open_date = current_time
        ticket.last_modified = current_time
        ticket.title = title
        ticket.description = description
        ticket_id = await db.tickets.insert(ticket=ticket)

        user = await db.users.get_by_id(user_id=message.chat.id)
        user.current_ticket_id = ticket_id
        await db.users.update(user=user)

        managers = await db.users.get_all_managers()
        if managers:
            from ..managers.tickets import get_accept_ticket_inline_keyboard
            user = await db.users.get_by_id(user_id=message.chat.id)
            tg_id, tg_name = user.id, user.tg_name
            for manager in managers:
                ticket_info = strs(lang=manager.lang).ticket_info(
                    id_=tg_id, tg_name=tg_name,
                    name=name, title=title, description=description
                )
                await message.bot.send_message(
                    chat_id=manager.id,
                    text=ticket_info,
                    reply_markup=await get_accept_ticket_inline_keyboard(ticket_id=ticket_id,
                                                                         lang=(await state.get_data())['lang'])
                )

        from .general import get_menu_reply_keyboard
        await message.answer(text=strs(lang=(await state.get_data())['lang']).ticket_opened,
                             reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang']))
        await state.clear()
    else:
        await message.answer(text=strs(lang=(await state.get_data())['lang']).ticket_ask_description_error)


@ticket_router.message(
    filters.Private(), filters.IsUser(),
    ((F.text == '/my_tickets') | (F.text.in_(my_tickets_btn))),
)
async def handle_my_tickets_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /my_tickets from user {message.chat.id}')
    user = await db.users.get_by_id(user_id=message.chat.id)
    current_ticket_id = user.current_ticket_id
    if current_ticket_id:
        ticket = await db.tickets.get_by_id(ticket_id=current_ticket_id)
        if ticket:
            name, title, description = ticket.username, ticket.title, ticket.description
            tg_id, tg_name = user.id, user.tg_name
            ticket_info = strs(lang=(await state.get_data())['lang']).ticket_info(
                id_=tg_id, tg_name=tg_name,
                name=name, title=title, description=description
            )
            await message.answer(
                text=strs(lang=(await state.get_data())['lang']).current_ticket_composition.format(ticket_info),
                reply_markup=await get_ticket_menu_inline_keyboard(is_current=True, ticket_id=ticket.id,
                                                                   lang=(await state.get_data())['lang'])
            )
            return

    await message.answer(
        text=strs(lang=(await state.get_data())['lang']).ticket_no_opened,
        reply_markup=await get_ticket_menu_inline_keyboard(is_current=False, lang=(await state.get_data())['lang'])
    )


@ticket_router.message(
    filters.Private(), filters.IsUser(), filters.InTicket(),
    filters.NotInState(), filters.IsRestricted()
)
async def handle_user_ticket_message(message: Message, state: FSMContext):
    bot_logger.info(f'Handling user ticket message of user {message.chat.id}')
    user = await db.users.get_by_id(user_id=message.chat.id)
    current_ticket_id = user.current_ticket_id
    ticket = await db.tickets.get_by_id(ticket_id=current_ticket_id)

    manager_id = ticket.manager_id
    if not manager_id:
        await message.answer(text=strs(lang=(await state.get_data())['lang']).ticket_no_manager)
        return
    await message.send_copy(chat_id=manager_id).as_(message.bot)

    from handlers.utils import CustomJSONEncoder
    current_date = datetime.now(timezone(timedelta(hours=3))) + timedelta(hours=3)
    message_info = loads(dumps(message.model_dump(), cls=CustomJSONEncoder))
    if ticket.content is str:
        ticket.content = ticket.content.replace('\'', '"').replace('None', 'null').replace('True', 'true').replace('False', 'false')
        ticket.content = loads(ticket.content)
    ticket.content.append(message_info)
    ticket.last_modified = current_date
    await db.tickets.update(ticket=ticket)

    if not message.text:
        media = (message.photo or message.video or message.audio or message.document or message.sticker
                 or message.voice or message.video_note or message.story or message.contact)
        if media:
            media_id = media[-1].file_id if isinstance(media, list) else media.file_id
            file_info = await message.bot.get_file(file_id=media_id)
            file_path = file_info.file_path
            media_url = f'https://api.telegram.org/file/bot{cf.bot["token"]}/{file_path}'

            destination_folder = cf.project['storage'] + f'/{ticket.id}'
            os.makedirs(destination_folder, exist_ok=True)

            media_info = f'{message.message_id} {message.media_group_id} {media_url}'
            with open(f'{destination_folder}/media_info.txt', 'a', encoding='utf-16') as f:
                f.write(media_info + '\n')
        else:
            bot_logger.warning('Do not support this type of message!')
