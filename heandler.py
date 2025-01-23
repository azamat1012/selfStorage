import telebot
from keyboards import create_consent_keyboard


def heandle_start(bot: telebot.TeleBot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        with open('agreement.txt', 'rb') as file:
            bot.send_document(message.chat.id, file)
        bot.send_message(message.chat.id, "Для продолжения работы с ботом необходимо принять соглашение "
                                        "об обработке персональных данных."
                                        "Прочтите соглашение и нажмите кнопку 'Принять'.",
                                        reply_markup=create_consent_keyboard()
                        )


