from . import *

# __router__ !DO NOT DELETE!
delete_tickets_router = Router()


# __states__ !DO NOT DELETE!


# __buttons__ !DO NOT DELETE!
async def get_sure_menu_inline_keyboard(month_amount: int) -> InlineKeyboardMarkup:
    button_list = [
        [InlineKeyboardButton(text='✔️ ', callback_data=f'yes_btn {month_amount}'),
         InlineKeyboardButton(text='✖️', callback_data='no_btn')],

    ]

    @delete_tickets_router.callback_query(F.data.startswith('yes_btn'))
    async def handle_yes_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling sure_menu yes button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        month_amount = int(data[1])

        count = 0
        tickets = await db.tickets.get_tickets_last_modified_ago(time_ago=month_amount, is_hours=False)
        if tickets:
            for ticket in tickets:
                await db.tickets.delete(ticket=ticket)
                count += 1

        user = await db.users.get_by_id(user_id=callback.message.chat.id)
        await callback.message.edit_text(
            text=strs(lang=user.lang).admin_delete,
            reply_markup=await get_delete_menu_inline_keyboard(
                should_notificate=user.should_notificate,
                lang=(await state.get_data())['lang']
            ))

        await callback.answer(
            text=strs(lang=user.lang).admin_delete_tickets(count=count),
        )

        await callback.answer()

    @delete_tickets_router.callback_query(F.data.startswith('no_btn'))
    async def handle_no_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling sure_menu no button callback from user {callback.message.chat.id}')
        user = await db.users.get_by_id(user_id=callback.message.chat.id)
        await callback.message.edit_text(
            text=strs(lang=user.lang).admin_delete,
            reply_markup=await get_delete_menu_inline_keyboard(
                lang=user.lang,
                should_notificate=user.should_notificate
            )
        )
        await callback.answer()

    return InlineKeyboardMarkup(inline_keyboard=button_list)


async def get_delete_menu_inline_keyboard(lang: str, should_notificate: bool) -> InlineKeyboardMarkup:
    button_list = [
        [InlineKeyboardButton(text=strs(lang=lang).month_btn_1, callback_data='month_btn 1'),
         InlineKeyboardButton(text=strs(lang=lang).month_btn_3, callback_data='month_btn 3')],
        [InlineKeyboardButton(text=strs(lang=lang).month_btn_6, callback_data='month_btn 6'),
         InlineKeyboardButton(text=strs(lang=lang).month_btn_12, callback_data='month_btn 12')]
    ]

    if should_notificate:
        button_list.append(
            [InlineKeyboardButton(text=strs(lang=lang).notification_btn_off, callback_data='notification_btn off')],
        )
    else:
        button_list.append(
            [InlineKeyboardButton(text=strs(lang=lang).notification_btn_on, callback_data='notification_btn on')],
        )

    button_list.append(
        [InlineKeyboardButton(text=strs(lang=lang).delete_btn, callback_data='delete_btn')],
    )

    @delete_tickets_router.callback_query(F.data.startswith('month_btn'))
    async def handle_month_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling delete_menu month button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        month_amount = int(data[1])

        count = 0
        tickets = await db.tickets.get_tickets_last_modified_ago(time_ago=month_amount, is_hours=False)
        if tickets:
            for ticket in tickets:
                await db.tickets.delete(ticket=ticket)
                count += 1

        await callback.message.edit_text(
            text=strs(lang=(await state.get_data())['lang']).admin_delete_sure.format(count),
            reply_markup=await get_sure_menu_inline_keyboard(month_amount=month_amount)
        )

        await callback.answer()

    @delete_tickets_router.callback_query(F.data.startswith('notification_btn'))
    async def handle_notification_button_callback(callback: CallbackQuery, state: FSMContext):
        bot_logger.info(f'Handling delete_menu notification button callback from user {callback.message.chat.id}')
        data = callback.data.split()
        action = data[1]

        user = await db.users.get_by_id(user_id=callback.message.chat.id)
        if action == 'on':
            user.should_notificate = True
            await db.users.update(user=user)
            await callback.message.edit_text(
                text=strs(lang=user.lang).admin_delete, reply_markup=await get_delete_menu_inline_keyboard(
                    lang=user.lang, should_notificate=True
                )
            )
            await callback.answer(text=strs(lang=user.lang).admin_delete_notification_on, show_alert=True)
        elif action == 'off':
            user.should_notificate = False
            await db.users.update(user=user)
            await callback.message.edit_text(
                text=strs(lang=user.lang).admin_delete, reply_markup=await get_delete_menu_inline_keyboard(
                    lang=user.lang, should_notificate=False
                )
            )
            await callback.answer(text=strs(lang=user.lang).admin_delete_notification_off, show_alert=True)

        await callback.answer()

    return InlineKeyboardMarkup(inline_keyboard=button_list)


# __chat__ !DO NOT DELETE!
@delete_tickets_router.message(
    filters.Private(), filters.IsAdmin(),
    ((F.text == '/delete_tickets') | (F.text.in_(delete_tickets_btn)))
)
async def handle_delete_tickets_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command /delete_tickets from user {message.chat.id}')
    user = await db.users.get_by_id(user_id=message.chat.id)
    await message.answer(text=strs(lang=user.lang).admin_delete, reply_markup=await get_delete_menu_inline_keyboard(
        lang=user.lang, should_notificate=user.should_notificate
    ))
