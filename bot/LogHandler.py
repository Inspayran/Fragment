import datetime
import telebot

from config import CHANNEL_ID


class LogHandler:
    def __init__(self, token, channel_id):
        self.token = token
        self.bot = telebot.TeleBot(token)
        self.channel_id = channel_id

    def send_message_to_channel(self, message):
        user_info = self.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        username = user_info.user.username
        current_time = datetime.datetime.now().strftime('%H:%M')
        current_date = datetime.datetime.now().strftime('%d.%m.%Y')
        self.bot.send_message(chat_id=CHANNEL_ID,
                              text=f'@{username}: {message.text}, \nВ: {current_time}, {current_date}')

    def send_parsing_update_message(self):
        current_time = datetime.datetime.now().strftime('%H:%M')
        current_date = datetime.datetime.now().strftime('%d.%m.%Y')
        self.bot.send_message(chat_id=CHANNEL_ID, text=f'Parsing and updating at {current_time}, {current_date}')
