# Third-party
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.exceptions import TelegramBadRequest
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

# Project
from bot import bot
import config as cf
from logger import bot_logger
from translations import strs
from database import db, UserModel
from .private.users.channel import get_channel_info_menu_inline_keyboard


class ChannelSubscriptionCheckMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user_info = data.get('event_from_user')
        user_id = user_info.id
        is_admin = user_id in cf.admin_ids
        channel_info = await db.preferences.get_by_key('channel_info')
        is_on = channel_info.value.get('is_on', True)
        if is_admin or not is_on:
            return await handler(event, data)

        if user_id:
            channel_info = await db.preferences.get_by_key('channel_info')
            id_, url = int(channel_info.value.get('id')), channel_info.value.get('url')
            lang = 'ru'
            user = await db.users.get_by_id(user_id)
            if user:
                lang = user.lang
            try:
                member_status = await bot.get_chat_member(chat_id=id_, user_id=user_id)
                if member_status.status.value in ['creator', 'administrator', 'member']:
                    return await handler(event, data)
                else:
                    await bot.send_message(
                        chat_id=user_id,
                        text=strs(lang=lang).middle_check_channel,
                        reply_markup=await get_channel_info_menu_inline_keyboard(user_id=user_id, lang=lang)
                    )
                    return CancelHandler()
            except TelegramBadRequest as e:
                bot_logger.error(e)
                await bot.send_message(
                    chat_id=user_id,
                    text=strs(lang=lang).middle_check_channel,
                    reply_markup=await get_channel_info_menu_inline_keyboard(user_id=user_id, lang=lang)
                )
                return CancelHandler()
            except Exception as e:
                bot_logger.error(e)
                await bot.send_message(chat_id=user_id, text=f'<b>Произошла внутреняя ошибка</b>\n\n{e}')
                return CancelHandler()


class InsertUserIfNotExistMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user_info = data.get('event_from_user')
        user_id = user_info.id
        full_name = user_info.full_name
        user_name = user_info.username
        user = await db.users.get_by_id(user_id=user_id)
        if not user:
            status = 'user'
            if user_id in cf.admin_ids:
                status = 'admin'
            user = UserModel()
            user.id = user_id
            user.tg_name = full_name
            user.url_name = user_name
            user.status = status
            await db.users.insert(user=user)

        return await handler(event, data)


class LanguageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user_info = data.get('event_from_user')
        user_id = user_info.id
        state = data.get('state')
        if state:
            user = await db.users.get_by_id(user_id=user_id)
            if user:
                await state.update_data({'lang': user.lang})

        return await handler(event, data)
