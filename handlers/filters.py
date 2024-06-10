# Third-party
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums.chat_type import ChatType

# Project
from database import db
from translations import strs
import config as cf


class IsUser(BaseFilter):  # Checks chat is private or not
    async def __call__(self, message: Message) -> bool:
        user = await db.users.get_by_id(user_id=message.from_user.id)

        if not user:
            return True

        if user.status and user.status == 'user':
            return True
        else:
            return False


class IsManagerOrAdmin(BaseFilter):  # Checks chat is private or not
    async def __call__(self, message: Message) -> bool:
        user = await db.users.get_by_id(user_id=message.from_user.id)
        if user:
            if user.status and user.status == 'manager' or message.from_user.id in cf.admin_ids:
                return True
        return False


class IsManager(BaseFilter):  # Checks chat is private or not
    async def __call__(self, message: Message) -> bool:
        user = await db.users.get_by_id(user_id=message.from_user.id)
        if user:
            if user.status and user.status == 'manager':
                return True
        return False


class IsAdmin(BaseFilter):  # Checks chat is private or not
    async def __call__(self, message: Message) -> bool:
        return message.chat.id in cf.admin_ids


class InTicket(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user = await db.users.get_by_id(user_id=message.from_user.id)
        if user.current_ticket_id:
            from translations import commands, reply_buttons
            text = message.text
            if text not in commands and text not in reply_buttons:
                return True
        return False


class IsRestricted(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user = await db.users.get_by_id(user_id=message.from_user.id)
        if user.is_banned:
            await message.answer(text=strs(lang=user.lang).restriction_banned_forever)
            return False

        if user.mute_time:
            await message.answer(text=strs(lang=user.lang).restriction_before(str(user.mute_time).split('.')[0]))
            return False

        return True


class NotInState(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        state = await state.get_state()
        return state is None


class Private(BaseFilter):  # Checks chat is private or not
    def __init__(self):
        self.chat_type = ChatType.PRIVATE.value

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
