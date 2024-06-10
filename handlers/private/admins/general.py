from . import *

# __router__ !DO NOT DELETE!
general_router = Router()


# __states__ !DO NOT DELETE!

# __buttons__ !DO NOT DELETE!
async def get_menu_reply_keyboard(lang: str) -> ReplyKeyboardMarkup:
    button_list = [
        [KeyboardButton(text=strs(lang=lang).change_faq_btn),
         KeyboardButton(text=strs(lang=lang).change_subscription_channel_btn)],
        [KeyboardButton(text=strs(lang=lang).find_user_btn),
         KeyboardButton(text=strs(lang=lang).my_tickets_btn)],
        [KeyboardButton(text=strs(lang=lang).send_mailing_btn),
         KeyboardButton(text=strs(lang=lang).start_msg_btn)],
        [KeyboardButton(text=strs(lang=lang).delete_tickets_btn),
         KeyboardButton(text=strs(lang=lang).manager_mode_btn)],
        [KeyboardButton(text=strs(lang=lang).change_close_release_btn)],
        [KeyboardButton(text=strs(lang=lang).choose_lang_btn)]
    ]

    return ReplyKeyboardMarkup(keyboard=button_list, resize_keyboard=True)


# __chat__ !DO NOT DELETE!
@general_router.message((Command('start')), filters.Private(), filters.IsAdmin(), )
async def handle_start_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /start from user {message.chat.id}')
    start_info = await db.preferences.get_by_key('start_message')
    start_msg = start_info.value.get('message')
    if start_msg == strs(lang=(await state.get_data())['lang']).general_start:
        await message.answer(
            text=start_msg,
            reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang']))
    else:
        await Message(**start_msg).send_copy(
            chat_id=message.chat.id, reply_markup=await get_menu_reply_keyboard((await state.get_data())['lang'])
        ).as_(message.bot)


@general_router.message(Command('help'), filters.Private(), filters.IsAdmin())
async def handle_help_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /help from user {message.chat.id}')
    await message.answer(
        text=strs((await state.get_data())['lang']).admin_general_help,
        reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang'])
    )


@general_router.message(
    filters.Private(), filters.IsAdmin(),
    ((F.text == '/to_manager') | (F.text.in_(manager_mode_btn)))
)
async def handle_to_manager_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /to_manager from user {message.chat.id}')

    user = await db.users.get_by_id(user_id=message.chat.id)
    user.status = 'manager'
    await db.users.update(user=user)

    from ..managers.general import get_menu_reply_keyboard
    await message.answer(text=strs(user.lang).admin_general_now_manager,
                         reply_markup=await get_menu_reply_keyboard(user_id=message.chat.id, lang=user.lang))
