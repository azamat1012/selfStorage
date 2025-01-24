import os
import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from inline_keyboards import (create_consent_keyboard,
                              create_my_order_keyboard,
                              create_box_info_keyboards,
                              create_statictic_info,)

from standart_keyboards import (create_first_keyboard_user,
                                create_second_keyboard_user,
                                create_third_keyboard_user,
                                create_fourth_keyboard_user,
                                create_first_keyboard_owner,)


# Создаем хранилище состояний
state_storage = StateMemoryStorage()
print("Создано хранилище состояний:", state_storage)  # Отладочный вывод


class UserStates(StatesGroup):
    enter_address = State()  # Состояние для ввода адреса


# Функция для сохранения адреса в файл
def save_to_file(user_id, address):
    try:
        with open('log_file.txt', 'a', encoding='utf-8') as file:
            file.write(f'User ID: {user_id}, Address: {address}\n')
        print("Адрес успешно сохранен в файл")  # Отладочный вывод
    except Exception as e:
        print(f"Ошибка при сохранении адреса: {e}")  # Отладочный вывод


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


# Обработчик нажатий инлайн-кнопки
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
        print(f"Получено сообщение: {message.text}")  # Отладочный вывод
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
        elif message.text == 'Оформить заказ':
            bot.send_message(message.chat.id,
                             'Выберите бокс из доступных',
                             reply_markup=create_third_keyboard_user())
        elif message.text == 'Посмотреть доступные боксы':
            bot.send_message(message.chat.id,
                             'Выберите способ доставки',
                             reply_markup=create_fourth_keyboard_user())
        elif message.text == 'Самовывоз':
            bot.send_message(message.chat.id,
                             """Список доступных боксов:
                                0. Бокс №0.
                                1. Бокс №1.
                                2. Бокс №2.    
                             """)
        elif message.text == 'Заказ курьера':
            print("Заказ курьера активирован")
            # Устанавливаем состояние для ввода адреса
            bot.set_state(message.from_user.id, UserStates.enter_address, message.chat.id)
            print(f"Состояние пользователя {message.from_user.id} изменено на enter_address")
            bot.send_message(
                message.chat.id,
                'Пожалуйста, введите ваш адрес для самовывоза'
            )
        elif message.text == 'Я владелец':
            bot.send_message(message.chat.id,
                             'Выбирайте нужный пункт',
                             reply_markup=create_first_keyboard_owner())
        elif message.text == 'Статистика':
            bot.send_message(message.chat.id,
                             'Сейчас будет важная статистика',
                             reply_markup=create_statictic_info())    


    # Обработчик для состояния ввода адреса
    @bot.message_handler(state=UserStates.enter_address)
    def save_address(message):
        print("Обработка состояния: enter_address")  # Отладочный вывод
        address = message.text
        print(f"Получен адрес: {address}")  # Отладочный вывод

        # Сохраняем адрес в файл
        save_to_file(message.from_user.id, address)

        # Завершаем состояние
        bot.delete_state(message.from_user.id, message.chat.id)
        print(f"Состояние пользователя {message.from_user.id} завершено")  # Отладочный вывод

        # Отправляем подтверждение
        bot.send_message(
            message.chat.id,
            f"Ваш адрес '{address}' сохранён. Спасибо!"
        )