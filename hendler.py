import telebot
from inline_keyboards import (create_consent_keyboard,
                              create_my_order_keyboard,
                              create_box_info_keyboards)

from standart_keyboards import (create_first_keyboard_user,
                                create_second_keyboard_user,)


def read_price():
    with open('price.txt', 'r', encoding='utf-8') as file:
        return file.read()
    

def read_rules():
    with open('storage_rules.txt', 'r', encoding='utf-8') as file:
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
        elif call.data == 'info_about_box':
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=create_box_info_keyboards()
            )
        elif call.data == 'box_name':
            bot.send_message(call.message.chat.id,
                            'Название вашего бокса: ...')
        elif call.data == 'storage_period':
            bot.send_message(call.message.chat.id, 
                            'Период хранения: 30 дней')
            
        
def handle_messages(bot: telebot.TeleBot):
    @bot.message_handler(func=lambda message: True)
    def handler_message(message):
        if message.text == 'Заказать бокс для вещей':
            bot.send_message(message.chat.id,
                             'Спасибо, что выбрали нас.',
                             reply_markup=create_second_keyboard_user())
        elif message.text == 'Прайс':
            bot.send_message(message.chat.id, read_price())
        elif message.text == 'Назад':
            bot.send_message(message.chat.id,
                             'Возвращаемся в Главное меню',
                             reply_markup=create_first_keyboard_user())
        elif message.text == 'Правила хранения':
            bot.send_message(message.chat.id, read_rules())
        elif message.text == 'Мои заказы':
            bot.send_message(message.chat.id,
                             'Выберите действие',
                             reply_markup=create_my_order_keyboard())
        


