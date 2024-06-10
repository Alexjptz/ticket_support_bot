from . import *

# Standard
from datetime import datetime, timezone, timedelta

# __router__ !DO NOT DELETE!
mute_router = Router()


# __states__ !DO NOT DELETE!
class MuteStates(StatesGroup):
    get_mute_time = State()


# __buttons__ !DO NOT DELETE!
async def _close_ticket(ticket_id: str):
    ticket = await db.tickets.get_by_id(ticket_id=ticket_id)
    if ticket:
        current_date = str(datetime.now(timezone(timedelta(hours=3))))
        close_date = ticket.close_date
        manager_id = ticket.manager_id
        if not close_date:
            ticket.close_date = current_date
            ticket.last_modified = current_date
            await db.tickets.update(ticket=ticket)
            if manager_id:
                manager = await db.users.get_by_id(user_id=manager_id)
                manager.current_ticket_id = None
                await db.users.update(user=manager)
            user = await db.users.get_by_id(user_id=ticket.user_id)
            user.current_ticket_id = None
            await db.users.update(user=user)


@mute_router.callback_query(F.data.startswith('ban_btn'))
async def handle_ban_button_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f'Handling user_actions ban button callback from user {callback.message.chat.id}')
    data = callback.data.split()
    user_id, ticket_id = int(data[1]), data[2]

    if ticket_id:
        await _close_ticket(ticket_id=ticket_id)

    user = await db.users.get_by_id(user_id=user_id)
    user.is_banned = True
    await db.users.update(user=user)

    await callback.bot.send_message(
        chat_id=user_id,
        text=strs(lang=user.lang).restriction_banned_forever
    )

    await callback.answer(
        text=strs(lang=(await state.get_data())['lang']).restriction_banned_successfully + strs(
            lang=user.lang).press_update_btn,
        show_alert=True)
    await callback.answer()


@mute_router.callback_query(F.data.startswith('unban_btn'))
async def handle_ban_button_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f'Handling user_actions ban button callback from user {callback.message.chat.id}')
    data = callback.data.split()
    user_id = int(data[1])

    user = await db.users.get_by_id(user_id=user_id)
    user.is_banned = False
    await db.users.update(user=user)

    await callback.bot.send_message(
        chat_id=user_id,
        text=strs(lang=user.lang).restriction_unbanned
    )

    await callback.answer(text=strs(
        lang=(await state.get_data())['lang']).restriction_unbanned_successfully + strs(
        lang=(await state.get_data())['lang']).press_update_btn,
                          show_alert=True)
    await callback.answer()


@mute_router.callback_query(F.data.startswith('ticket_mute'), filters.IsManagerOrAdmin())
async def handle_mute_button_callback(callback: CallbackQuery, state: FSMContext):
    bot_logger.info(f'Handling ticket_menu mute button callback from user {callback.message.chat.id}')
    data = callback.data.split()
    user_id = ticket_id = None
    if len(data) == 2:
        ticket_id = data[1]
    elif len(data) == 3:
        ticket_id, user_id = data[1], int(data[2])

    from ..users import get_decline_reply_keyboard
    await callback.message.answer(text=strs(lang=(await state.get_data())['lang']).ticket_get_mute,
                                  reply_markup=await get_decline_reply_keyboard(lang=(await state.get_data())['lang']))

    await state.update_data({'ticket_id': ticket_id, 'user_id': user_id})
    await state.set_state(MuteStates.get_mute_time.state)

    await callback.answer()


# __chat__ !DO NOT DELETE!
@ticket_router.message(MuteStates.get_mute_time)
async def handle_get_mute_time_state(message: Message, state: FSMContext):
    bot_logger.info(f'Handling states MuteStates.get_mute_time from user {message.chat.id}')
    mute_mins = message.text
    if mute_mins and mute_mins.isdigit() and 0 <= int(mute_mins) <= 1440:
        data = await state.get_data()
        ticket_id = data['ticket_id']
        user_id = data['user_id']

        if int(mute_mins) == 0:
            user = await db.users.get_by_id(user_id=user_id)
            user.mute_time = None
            await db.users.update(user=user)

            user = await db.users.get_by_id(user_id=user_id)
            await message.bot.send_message(
                chat_id=user_id,
                text=strs(lang=user.id).restriction_unmuted
            )

            from .general import get_menu_reply_keyboard
            await message.answer(
                text=strs(lang=(await state.get_data())['lang']).restriction_unmuted_succesfully,
                reply_markup=await get_menu_reply_keyboard(user_id=message.chat.id,
                                                           lang=(await state.get_data())['lang'])
            )

            await state.clear()
            return

        if ticket_id != 'None':
            ticket = await db.tickets.get_by_id(ticket_id=ticket_id)
            await _close_ticket(ticket_id=ticket_id)
            user_id = ticket.user_id

        current_time = datetime.now(timezone(timedelta(hours=3)))
        user = await db.users.get_by_id(user_id=user_id)
        user.mute_time = current_time + timedelta(minutes=int(mute_mins)) + timedelta(hours=3)
        await db.users.update(user=user)

        await message.bot.send_message(
            chat_id=user_id,
            text=strs(lang=user.lang).restirction_get_muted(mute_mins)
        )

        from .general import get_menu_reply_keyboard
        await message.answer(
            text=strs(lang=(await state.get_data())['lang']).restriction_succesfully(mute_mins),
            reply_markup=await get_menu_reply_keyboard(user_id=message.chat.id, lang=(await state.get_data())['lang'])
        )

        await state.clear()
    else:
        await message.answer(text=strs(lang=(await state.get_data())['lang']).ticket_get_mute_error)
