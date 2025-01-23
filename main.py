from dotenv import load_dotenv
import os
import telebot
from hendler import hendle_start, handle_callbacks


def main():
    load_dotenv()

    token_tg = os.environ['TG_TOKEN']
    bot = telebot.TeleBot(token_tg)

    hendle_start(bot)
    handle_callbacks(bot) 

    bot.polling()


if __name__ == "__main__":
    main()
