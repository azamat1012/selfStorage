import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import django
import telebot

#Здесь настройка джанго: у меня почему-то только так работает
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend.settings")
django.setup()

try:
    from backend.handlers import handle_start, handle_callbacks, handle_messages
except ImportError as e:
    print(e)

def main():
    load_dotenv()
    token_tg = os.getenv('TG_BOT_TOKEN')
    bot = telebot.TeleBot(token_tg)
    handle_start(bot)
    handle_messages(bot)
    handle_callbacks(bot)
    try:
        bot.polling()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
