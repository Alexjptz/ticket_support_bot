from . import *

# __router__ !DO NOT DELETE!
release_close_router = Router()


# __states__ !DO NOT DELETE!
class ChangeTimeStates(StatesGroup):
    get_time = State()


# __buttons__ !DO NOT DELETE!


# __chat__ !DO NOT DELETE!
@release_close_router.message(
    filters.Private(), filters.IsAdmin(),
    ((F.text == '/change_release_close_time') |
     (F.text.in_(change_close_release_btn)))
)
async def handle_change_release_close_time_command(message: Message, state: FSMContext):
    bot_logger.info(f'Handling command //change_release_close_time from user {message.chat.id}')
    release = await db.preferences.get_by_key('release_hours')
    release_hours = release.value.get('hours')
    close = await db.preferences.get_by_key('close_hours')
    close_hours = close.value.get('hours')

    text = strs(lang=(await state.get_data())['lang']).release_composite.format(release_hours)
    text += strs(lang=(await state.get_data())['lang']).close_composite.format(close_hours)

    from . import get_decline_reply_keyboard
    await message.answer(text=text)
    await message.answer(text=strs(lang=(await state.get_data())['lang']).admin_release_close_ask_time,
                         reply_markup=await get_decline_reply_keyboard(lang=(await state.get_data())['lang']))
    await state.set_state(state=ChangeTimeStates.get_time.state)


@release_close_router.message(ChangeTimeStates.get_time)
async def handle_get_time_state(message: Message, state: FSMContext):
    bot_logger.info(f'Handling states ChangeTimeStates.get_time from user {message.chat.id}')
    import re

    text = message.text
    match = re.match('^(\w+) +(\d+)$', text)
    if text and match:
        action, hours = match.groups()
        action = action.lower()
        if action in ['закрытие', 'closing', 'releasing', 'освобождение']:
            from .general import get_menu_reply_keyboard

            if action == 'закрытие' or action == 'closing':
                close_hours = await db.preferences.get_by_key(key='close_hours')
                close_hours.value = {'hours': int(hours)}
                await db.preferences.update(preference=close_hours)
                await message.answer(text=strs(lang=(await state.get_data())['lang']).admin_close_updated,
                                     reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang']))
            elif action == 'освобождение' or action == 'releasing':
                release_hours = await db.preferences.get_by_key(key='release_hours')
                release_hours.value = {'hours': int(hours)}
                await db.preferences.update(preference=release_hours)
                await message.answer(text=strs(lang=(await state.get_data())['lang']).admin_release_updated,
                                     reply_markup=await get_menu_reply_keyboard(lang=(await state.get_data())['lang']))
            await state.clear()
            return

    await message.answer(text=strs(lang=(await state.get_data())['lang']).admin_release_close_ask_time_error)
