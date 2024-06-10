from . import *

# Standard
from json import loads, dumps

# Project
from .general import get_menu_reply_keyboard
from handlers.utils import CustomJSONEncoder

# __router__ !DO NOT DELETE!
mailing_router = Router()


# __states__ !DO NOT DELETE!
class MailingStates(StatesGroup):
    get_msg = State()
    get_link = State()


# __buttons__ !DO NOT DELETE!
async def get_mailing_msg_menu_inline_keyboard(lang: str, show_add_link: bool = True) -> InlineKeyboardMarkup:
    button_list = [
        [InlineKeyboardButton(text=strs(lang=lang).send_mailing_message_btn, callback_data='mailing_send_btn')],
    ]

    if show_add_link:
        button_list.append(
            [InlineKeyboardButton(text=strs(lang=lang).mailing_add_link_btn, callback_data=f'mailing_add_link_btn')])

    button_list.append(
        [InlineKeyboardButton(text=strs(lang=lang).mailing_delete_btn, callback_data='mailing_delete_btn')]
    )

    @mailing_router.callback_query(F.data.startswith('mailing_delete_btn'))
    async def handle_mailing_delete_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling add_link mailing_delete button callback from user {callback.message.chat.id}')
        await db.preferences.delete(preference=(await db.preferences.get_by_key(key='preference_message')))
        await callback.message.delete()
        await callback.message.answer(
            text=strs(lang=(await state.get_data())['lang']).use_help,
            reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang'])
        )
        await callback.answer()

    @mailing_router.callback_query(F.data.startswith('mailing_add_link_btn'))
    async def handle_link_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling add_link link button callback from user {callback.message.chat.id}')

        from . import get_decline_reply_keyboard
        await callback.message.answer(
            text=strs(lang=(await state.get_data())['lang']).admin_mailing_add_link,
            reply_markup=await get_decline_reply_keyboard(lang=(await state.get_data())['lang']))
        await state.set_state(MailingStates.get_link.state)
        await callback.answer()

    @mailing_router.callback_query(F.data.startswith('mailing_send_btn'))
    async def handle_mailing_send_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling add_link mailing_send button callback from user {callback.message.chat.id}')

        users = await db.users.get_all()
        cur_user = await db.users.get_by_id(user_id=callback.message.chat.id)
        count = 0
        if users:
            for user in users:
                if user.id != callback.message.chat.id:
                    message = callback.message
                    if message.reply_markup.inline_keyboard:
                        if message.reply_markup.inline_keyboard[-1][-1].text != strs(lang=cur_user.lang).mailing_delete_btn:
                            message.reply_markup.inline_keyboard = [message.reply_markup.inline_keyboard[-1]]
                        else:
                            message.reply_markup.inline_keyboard = []
                    await message.send_copy(
                        chat_id=user.id,
                    ).as_(callback.bot)

                    count += 1
        if count == 0:
            await callback.message.answer(
                text=strs(lang=(await state.get_data())['lang']).admin_general_no_users,
                reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang']))
        else:
            await callback.message.answer(
                text=strs(lang=(await state.get_data())['lang']).admin_general_mailing_successful,
                reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang']))

        await db.preferences.delete(preference=(await db.preferences.get_by_key(key='preference_message')))
        await callback.message.delete()
        await callback.answer()

    return InlineKeyboardMarkup(inline_keyboard=button_list)


# __chat__ !DO NOT DELETE!
@mailing_router.message(
    filters.Private(), filters.IsAdmin(),
    ((F.text == '/mailing') | (F.text.in_(send_mailing_btn)))
)
async def handle_mailing_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /mailing from user {message.chat.id}')

    from . import get_decline_reply_keyboard
    await message.answer(text=strs(lang=(await state.get_data())['lang']).admin_general_ask_mailing_msg,
                         reply_markup=await get_decline_reply_keyboard(lang=(await state.get_data())['lang']))

    await state.set_state(MailingStates.get_msg.state)


@mailing_router.message(MailingStates.get_link)
async def handle_get_msg_state(message: Message, state: FSMContext):
    bot_logger.info(f'Handling states MailingStates.get_msg from user {message.chat.id}')

    text = message.text
    if text:
        entities = message.entities
        if entities:
            for entity in message.entities:
                name = ' '.join(text.split()[:-1])
                url = text.split()[-1]
                if (entity.type == 'url' or entity.type == 'text_link') and len(url.strip().split(' ')) == 1:
                    info = await db.preferences.get_by_key('preference_message')
                    msg_info = info.value.get('content')
                    send_msg = Message(**msg_info)
                    markup = await get_mailing_msg_menu_inline_keyboard(show_add_link=False,
                                                                        lang=(await state.get_data())['lang'])
                    markup.inline_keyboard.append(
                        [InlineKeyboardButton(text=name, url=url)]
                    )

                    await send_msg.send_copy(
                        chat_id=message.chat.id,
                        reply_markup=markup
                    ).as_(message.bot)
                    await state.clear()
                    return

    await message.answer(text=strs(lang=(await state.get_data())['lang']).admin_mailing_add_link_error)


@mailing_router.message(MailingStates.get_msg)
async def handle_get_msg_state(message: Message, state: FSMContext):
    bot_logger.info(f'Handling states MailingStates.get_msg from user {message.chat.id}')

    await message.delete()
    await message.answer(text=strs(lang=(await state.get_data())['lang']).mailing_what_to_do,
                         reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang']))
    msg = await message.send_copy(
        chat_id=message.chat.id,
        reply_markup=await get_mailing_msg_menu_inline_keyboard(lang=(await state.get_data())['lang'])
    )
    msg_info = loads(dumps(msg.model_dump(), cls=CustomJSONEncoder))

    pref = await db.preferences.get_by_key(key='preference_message')
    if pref:
        await db.preferences.delete(preference=pref)
    preference_message = PreferenceModel()
    preference_message.key = 'preference_message'
    preference_message.value = {'content': msg_info}
    await db.preferences.insert(preference=preference_message)

    await state.clear()
