from dotenv import load_dotenv
import os
import telebot
from heandler import heandle_start


def main():
    load_dotenv()

    token_tg = os.environ['TG_TOKEN']
    bot = telebot.TeleBot(token_tg)

    heandle_start(bot)

    bot.polling()


if __name__ == "__main__":
    main()
