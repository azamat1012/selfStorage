import telebot
from keyboards import (create_consent_keyboard,
                       create_back_buttom, create_first_keyboard_user)


def read_price():
    with open('price', 'r', encoding='utf-8') as file:
        return file.read()
    
    
def hendle_start(bot: telebot.TeleBot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        with open('agreement.txt', 'rb') as file:
            bot.send_document(message.chat.id, file)
        bot.send_message(message.chat.id, "Для продолжения работы с ботом необходимо принять соглашение "
                                        "об обработке персональных данных."
                                        "Прочтите соглашение и нажмите кнопку 'Принять'.",
                                        reply_markup=create_consent_keyboard()
                        )


# Обработчик нажатий  инлайн-кнопки
def handle_callbacks(bot: telebot.TeleBot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        if call.data == 'accept':
            bot.send_message(call.message.chat.id, "Спасибо! Вы приняли соглашение. Теперь вы можете продолжить.",
                             reply_markup=create_first_keyboard_user())
        elif call.data == 'reject':
            bot.send_message(call.message.chat.id,
                             "Вы не приняли соглашение. Для продолжения работы с ботом необходимо дать согласие.")
        

def handle_messages(bot: telebot.Telebot):
    @bot.message_handler(func=lambda message:True)
    def handler_message(message):
        if message.text == 'Прайс':



