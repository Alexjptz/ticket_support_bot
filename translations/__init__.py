# Project
from .ru_strs import RuTranslation
from .en_strs import EnTranslation

# Standard
from enum import Enum


class Language(Enum):
    RU = 'ru'
    EN = 'en'


def strs(lang: str):
    match lang:
        case Language.RU.value:
            return RuTranslation
        case Language.EN.value:
            return EnTranslation


decline_btn = [RuTranslation.decline_btn, EnTranslation.decline_btn]
delete_tickets_btn = [RuTranslation.delete_tickets_btn, EnTranslation.delete_tickets_btn]
change_faq_btn = [RuTranslation.change_faq_btn, EnTranslation.change_faq_btn]
faq_btn = [RuTranslation.faq_btn, EnTranslation.faq_btn]
change_subscription_channel_btn = [RuTranslation.change_subscription_channel_btn, EnTranslation.change_subscription_channel_btn]
find_user_btn = [RuTranslation.find_user_btn, EnTranslation.find_user_btn]
my_tickets_btn = [RuTranslation.my_tickets_btn, EnTranslation.my_tickets_btn]
send_mailing_btn = [RuTranslation.send_mailing_btn, EnTranslation.send_mailing_btn]
start_msg_btn = [RuTranslation.start_msg_btn, EnTranslation.start_msg_btn]
change_close_release_btn = [RuTranslation.change_close_release_btn, EnTranslation.change_close_release_btn]
manager_mode_btn = [RuTranslation.manager_mode_btn, EnTranslation.manager_mode_btn]
admin_mode_btn = [RuTranslation.admin_mode_btn, EnTranslation.admin_mode_btn]
opened_tickets_btn = [RuTranslation.opened_tickets_btn, EnTranslation.opened_tickets_btn]
create_ticket_btn = [RuTranslation.create_ticket_btn, EnTranslation.create_ticket_btn]
choose_lang_btn = [RuTranslation.choose_lang_btn, EnTranslation.choose_lang_btn]


reply_buttons = RuTranslation.reply_buttons + EnTranslation.reply_buttons

commands = [
    '/start', '/help', '/create_ticket', '/my_tickets', '/faq',
    '/opened_tickets', '/search', '/to_admin', '/change_faq',
    '/change_channel', '/mailing', '/start_msg', '/change_release_close_time',
    '/delete_tickets', '/to_manager', '/lang'
]