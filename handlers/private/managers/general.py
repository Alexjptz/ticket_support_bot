from . import *

# __router__ !DO NOT DELETE!
general_router = Router()


# __states__ !DO NOT DELETE!


# __buttons__ !DO NOT DELETE!
async def get_menu_reply_keyboard(user_id: int, lang: str) -> ReplyKeyboardMarkup:
    button_list = [
        [KeyboardButton(text=strs(lang=lang).opened_tickets_btn),
         KeyboardButton(text=strs(lang=lang).my_tickets_btn)],
        [KeyboardButton(text=strs(lang=lang).find_user_btn),
         KeyboardButton(text=strs(lang=lang).faq_btn)],
        [KeyboardButton(text=strs(lang=lang).choose_lang_btn)]
    ]

    if user_id in cf.admin_ids:
        button_list.append([KeyboardButton(text=strs(lang=lang).admin_mode_btn)], )

    return ReplyKeyboardMarkup(keyboard=button_list, resize_keyboard=True)


# __chat__ !DO NOT DELETE!
@general_router.message((Command('start')), filters.Private(), filters.IsManager())
async def handle_start_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /start from user {message.chat.id}')
    start_info = await db.preferences.get_by_key('start_message')
    start_msg = start_info.value.get('message')
    if start_msg == strs(lang=(await state.get_data())['lang']).general_start:
        await message.answer(text=start_msg,
                             reply_markup=await get_menu_reply_keyboard(
                                 user_id=message.chat.id,
                                 lang=(await state.get_data())['lang'])
                             )
    else:
        await Message(**start_msg).send_copy(
            chat_id=message.chat.id,
            reply_markup=await get_menu_reply_keyboard(user_id=message.chat.id, lang=(await state.get_data())['lang'])
        ).as_(message.bot)


@general_router.message(
    filters.Private(),
    ((F.text == '/to_admin') | (F.text.in_(admin_mode_btn)))
)
async def handle_to_admin_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /to_admin from user {message.chat.id}')
    if message.chat.id in cf.admin_ids:
        user = await db.users.get_by_id(user_id=message.chat.id)
        user.status = 'admin'
        await db.users.update(user=user)
        from ..admins.general import get_menu_reply_keyboard
        await message.answer(text=strs(lang=(await state.get_data())['lang']).manager_general_status_updated,
                             reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang']))
    else:
        await message.answer(text=strs(lang=(await state.get_data())['lang']).manager_general_status_updated_error)


@general_router.message(Command('help'), filters.Private(), filters.IsManager())
async def handle_help_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /help from user {message.chat.id}')
    await message.answer(text=strs(lang=(await state.get_data())['lang']).manager_general_help,
                         reply_markup=await get_menu_reply_keyboard(user_id=message.chat.id,
                                                                    lang=(await state.get_data())['lang']))
