from config import TOKEN
from scraper.scraper import Parser
from bot.telegram_bot import TelegramBot


def main():
    parser = Parser()
    parser.start()

    bot = TelegramBot(TOKEN)
    bot.start()


if __name__ == '__main__':
    main()
