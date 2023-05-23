import datetime

import requests
import telebot

from bot.LogHandler import LogHandler
from scraper.scraper import Parser
from config import TOKEN, CHANNEL_ID

from ton.price import ton_price

bot = telebot.TeleBot(TOKEN)


class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.bot = telebot.TeleBot(token)
        self.log_handler = LogHandler(self.token, CHANNEL_ID)
        self.user_last_request = {}

    def start(self):
        @self.bot.message_handler(commands=['start'])
        def pressed_btn_start(message):
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            button = telebot.types.KeyboardButton(text='Получить данные')
            keyboard.add(button)
            self.bot.send_message(chat_id=message.chat.id, text='Нажми кнопку, чтобы получить данные',
                                  reply_markup=keyboard)
            self.log_handler.send_message_to_channel(message)

        @self.bot.message_handler(func=lambda message: message.text == 'Получить данные')
        def send_data(message):
            user_id = message.from_user.id
            current_time = datetime.datetime.now()

            if user_id in self.user_last_request:
                last_request_time = self.user_last_request[user_id]
                time_diff = current_time - last_request_time

                # Ограничение времени между запросами (в данном случае 1 минута)
                if time_diff.seconds < 1:
                    self.bot.send_message(chat_id=message.chat.id,
                                          text=f'Пожалуйста не отправляйте запросы так быстро.')
                    return

            self.user_last_request[user_id] = current_time

            numbers_dict = Parser.cached_numbers
            text = ' | '.join([f"{k}: {v}" for k, v in numbers_dict.items()])

            toncoin = ton_price()
            text += f'\n\n{toncoin}'

            with open('diagram.png', 'rb') as photo:
                self.bot.send_photo(chat_id=message.chat.id, photo=photo, caption=text)
                self.log_handler.send_message_to_channel(message)

        @self.bot.message_handler(func=lambda message: True)
        def send_log(message):
            self.log_handler.send_message_to_channel(message)

        self.bot.polling(none_stop=True)
