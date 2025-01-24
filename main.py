from dotenv import load_dotenv
import os
import telebot
from hendler import hendle_start, handle_callbacks, handle_messages, state_storage


def main():
    load_dotenv()

    token_tg = os.environ['TG_TOKEN']
    bot = telebot.TeleBot(token_tg, state_storage=state_storage)

    hendle_start(bot)
    handle_callbacks(bot)
    handle_messages(bot) 

    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()

    bot.polling()


if __name__ == "__main__":
    main()
