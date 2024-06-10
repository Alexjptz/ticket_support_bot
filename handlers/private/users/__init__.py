# Third-party
from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ErrorEvent, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

# Project
import handlers.filters as filters
import handlers.middleware as middle
import config as cf
from translations import *
from database import db, UserModel, TicketModel, PreferenceModel
from logger import bot_logger

# Routers
from .general import general_router
from .tickets import ticket_router
from .channel import channel_router

user_router = Router()
sub_routers = [
    general_router, ticket_router, channel_router
]

for router in sub_routers:
    router.message.middleware(middle.ChannelSubscriptionCheckMiddleware())
    router.message.middleware(middle.InsertUserIfNotExistMiddleware())
    router.message.middleware(middle.LanguageMiddleware())
    router.callback_query.middleware(middle.LanguageMiddleware())

user_router.include_routers(*sub_routers)
user_router.callback_query.middleware(middle.LanguageMiddleware())
user_router.message.middleware(middle.LanguageMiddleware())


async def get_decline_reply_keyboard(lang: str) -> ReplyKeyboardMarkup:
    button_list = [
        [KeyboardButton(text=strs(lang=lang).decline_btn)],
    ]

    return ReplyKeyboardMarkup(keyboard=button_list, resize_keyboard=True, one_time_keyboard=True)


@user_router.message(filters.IsUser(), F.text.in_(decline_btn))
async def handle_decline_message(message: Message, state: FSMContext):
    bot_logger.info(f'Handling decline state from user {message.from_user.id}')
    from .general import get_menu_reply_keyboard
    lang = (await state.get_data())['lang']
    await message.answer(
        text=strs(lang=lang).decline_msg,
        reply_markup=await get_menu_reply_keyboard(lang=lang)
    )
    await state.clear()
