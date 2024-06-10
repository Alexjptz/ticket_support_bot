from . import *

# Project
from handlers.utils import make_up_user_info

# __router__ !DO NOT DELETE!
search_router = Router()


# __states__ !DO NOT DELETE!
class UserInfoStates(StatesGroup):
    get_user_info = State()


# __buttons__ !DO NOT DELETE!
async def get_user_actions_inline_keyboard(
        lang: str, user_id: int, ticket_id: str, user_is_manager: bool, is_user_admin: bool = False
) -> InlineKeyboardMarkup | None:
    if user_is_manager and not is_user_admin:
        return

    button_list = []

    if not user_is_manager:
        button_list.append(
            [InlineKeyboardButton(text=strs(lang=lang).mute_btn, callback_data=f'ticket_mute {ticket_id} {user_id}')])

    button_list.append(
        [InlineKeyboardButton(text=strs(lang=lang).user_tickets_btn,
                              callback_data=f'ticket_user_tickets {ticket_id} {user_id} {int(user_is_manager)}')],
    )

    if is_user_admin:
        user = await db.users.get_by_id(user_id)
        is_banned = user.is_banned
        if not is_banned:
            is_banned = False

        if not is_banned:
            button_list.append(
                [InlineKeyboardButton(text=strs(lang=lang).ban_btn, callback_data=f'ban_btn {user_id} {ticket_id}')]
            )
        else:
            button_list.append(
                [InlineKeyboardButton(text=strs(lang=lang).unban_btn, callback_data=f'unban_btn {user_id}')]
                # In restriction.py
            )

        if user_is_manager:
            button_list.append(
                [InlineKeyboardButton(text=strs(lang=lang).make_ordinary_btn,
                                      callback_data=f'make_user user {user_id}')]
            )
        else:
            button_list.append(
                [InlineKeyboardButton(text=strs(lang=lang).make_manager_btn,
                                      callback_data=f'make_user manager {user_id}')]
            )

        button_list.append(
            [InlineKeyboardButton(text=strs(lang=lang).update_btn,
                                  callback_data=f'search_update_btn {user_id} {ticket_id} {int(user_is_manager)} {int(is_user_admin)}')],
        )
        button_list.append(
            [InlineKeyboardButton(text=strs(lang=lang).delete_btn, callback_data='delete_btn')]
        )

    @ticket_data_router.callback_query(filters.IsManagerOrAdmin(), F.data.startswith('make_user'))
    async def handle_change_user_status_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(
            f'Handling ticket_change_data change user status button callback from user {callback.message.chat.id}'
        )
        data = callback.data.split()
        status, user_id = data[1], int(data[2])

        user = await db.users.get_by_id(user_id=user_id)
        user.status = status
        await db.users.update(user=user)

        if status == 'manager':
            from ..managers.general import get_menu_reply_keyboard
            text = strs(lang=user.lang).search_manager_now
            markup = await get_menu_reply_keyboard(user_id=callback.message.chat.id,
                                                   lang=(await state.get_data())['lang'])
        else:
            from ..users.general import get_menu_reply_keyboard
            text = strs(lang=user.lang).search_user_now
            markup = await get_menu_reply_keyboard(lang=(await state.get_data())['lang'])

        await callback.bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=markup
        )

        await callback.answer(
            text=strs(lang=(await state.get_data())['lang']).data_update + strs(
                lang=(await state.get_data())['lang']).press_update_btn,
            show_alert=True)

    @ticket_data_router.callback_query(filters.IsManagerOrAdmin(), F.data.startswith('search_update_btn'))
    async def handle_change_title_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(
            f'Handling ticket_change_data update button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        user_id, ticket_id = int(data[1]), data[2]
        user_is_manager, is_user_admin = bool(int(data[3])), bool(int(data[4]))

        user = await db.users.get_by_id(user_id=user_id)
        is_manager, info = await make_up_user_info(user=user, lang=(await state.get_data())['lang'])
        if info != callback.message.html_text:
            await callback.message.edit_text(
                text=info,
                reply_markup=await get_user_actions_inline_keyboard(
                    user_id=user_id, ticket_id=ticket_id,
                    user_is_manager=is_manager, is_user_admin=is_user_admin,
                    lang=(await state.get_data())['lang']
                )
            )
        await callback.answer()

    return InlineKeyboardMarkup(inline_keyboard=button_list)


# __chat__ !DO NOT DELETE!
@search_router.message(
    filters.Private(), filters.IsManagerOrAdmin(),
    ((F.text == '/search') | (F.text.in_(find_user_btn)))
)
async def handle_search_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /search from user {message.chat.id}')

    from . import get_decline_reply_keyboard
    await message.answer(text=strs(lang=(await state.get_data())['lang']).search_ask_info,
                         reply_markup=await get_decline_reply_keyboard(lang=(await state.get_data())['lang']))

    await state.set_state(UserInfoStates.get_user_info.state)


@search_router.message(UserInfoStates.get_user_info)
async def handle_get_user_info_state(message: Message, state: FSMContext):
    bot_logger.info(f'Handling states UserInfoStates.get_user_info from user {message.chat.id}')
    from .general import get_menu_reply_keyboard
    user = await db.users.get_by_id(user_id=message.chat.id)
    is_user_admin = user.status == 'admin'

    from .general import get_menu_reply_keyboard as manager_menu_kb
    from ..admins.general import get_menu_reply_keyboard as admin_menu_kb
    markup = await manager_menu_kb(user_id=message.chat.id, lang=(await state.get_data())['lang'])
    if is_user_admin:
        markup = await admin_menu_kb(lang=(await state.get_data())['lang'])

    info = message.text
    if info:
        user_by_id = None
        if info.isdigit():
            user_by_id = await db.users.get_by_id(user_id=int(info))
        user_by_name = await db.users.get_by_tg_name(tg_name=info)
        user_by_url = await db.users.get_by_url_name(url_name=info[1:])

        user = user_by_id or user_by_name or user_by_url
        if user:
            await message.answer(text=strs(lang=(await state.get_data())['lang']).user_found, reply_markup=markup)
            is_manager, info = await make_up_user_info(user=user, lang=(await state.get_data())['lang'])
            await message.answer(text=info, reply_markup=await get_user_actions_inline_keyboard(
                ticket_id=user.current_ticket_id, user_id=int(user.id),
                user_is_manager=is_manager, is_user_admin=is_user_admin,
                lang=(await state.get_data())['lang']
            ))
        else:
            await message.answer(
                text=strs(lang=(await state.get_data())['lang']).search_not_found,
                reply_markup=await get_menu_reply_keyboard(user_id=message.chat.id,
                                                           lang=(await state.get_data())['lang'])
            )

        await state.clear()
        return

    await message.answer(text=strs(lang=(await state.get_data())['lang']).search_ask_info_error)
