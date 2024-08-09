from . import *

# __router__ !DO NOT DELETE!
general_router = Router()


# __states__ !DO NOT DELETE!


# __buttons__ !DO NOT DELETE!
async def get_menu_reply_keyboard(lang: str) -> ReplyKeyboardMarkup:
    button_list = [
        [KeyboardButton(text=strs(lang=lang).create_ticket_btn),
         KeyboardButton(text=strs(lang=lang).my_tickets_btn)],
        [KeyboardButton(text=strs(lang=lang).faq_btn)],
        [KeyboardButton(text=strs(lang=lang).choose_lang_btn)]

    ]

    return ReplyKeyboardMarkup(keyboard=button_list, resize_keyboard=True)


async def get_choose_lang_inline_keyboard(lang: str) -> InlineKeyboardMarkup:
    button_list = [
        [InlineKeyboardButton(text='🇷🇺', callback_data='lang_btn ru'),
         InlineKeyboardButton(text='🇬🇧', callback_data='lang_btn en')],

    ]

    @general_router.callback_query(F.data.startswith('lang_btn'))
    async def handle_lang_ru_button_callback(callback: CallbackQuery, state: FSMContext):
        global get_menu_reply_keyboard
        bot_logger.info(f'Handling choose_lang lang_ru button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        lang = data[1]

        user = await db.users.get_by_id(user_id=callback.message.chat.id)
        match lang:
            case Language.RU.value:
                user.lang = lang
                await db.users.update(user=user)
            case Language.EN.value:
                user.lang = lang
                await db.users.update(user=user)

        keyboard = None
        match user.status:
            case 'admin':
                from ..admins.general import get_menu_reply_keyboard
                keyboard = await get_menu_reply_keyboard(lang=user.lang)
            case 'manager':
                from ..managers.general import get_menu_reply_keyboard
                keyboard = await get_menu_reply_keyboard(user_id=user.id, lang=user.lang)
            case 'user':
                keyboard = await get_menu_reply_keyboard(lang=user.lang)

        if strs(lang=lang).general_lang != callback.message.text:
            await callback.message.edit_text(text=strs(lang=lang).general_lang,
                                             reply_markup=callback.message.reply_markup)
        await callback.message.answer(text=strs(lang=lang).language_updated, reply_markup=keyboard)
        await callback.answer()

    return InlineKeyboardMarkup(inline_keyboard=button_list)


# __chat__ !DO NOT DELETE!
@general_router.message((Command('start')), filters.Private(), filters.IsUser())
async def handle_start_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /start from user {message.chat.id}')

    start_info = await db.preferences.get_by_key('start_message')
    start_msg = start_info.value.get('message')
    if start_msg == strs(lang=(await state.get_data())['lang']).general_start:
        await message.answer(text=start_msg,
                             reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang']))
    else:
        await Message(**start_msg).send_copy(
            chat_id=message.chat.id, reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang'])
        ).as_(message.bot)


@general_router.message(Command('help'), filters.Private(), filters.IsUser())
async def handle_help_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /help from user {message.chat.id}')
    await message.answer(text=strs(lang=(await state.get_data())['lang']).general_help,
                         reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang']))


@general_router.message(
    filters.Private(),
    (F.text == '/lang') | (F.text.in_(choose_lang_btn))
)
async def handle_lang_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /lang from user {message.chat.id}')
    lang = (await state.get_data())['lang']
    await message.answer(text=strs(lang=lang).general_lang,
                         reply_markup=await get_choose_lang_inline_keyboard(lang=lang))
