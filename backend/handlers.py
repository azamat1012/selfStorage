import os
from .keyboards import create_consent_keyboard, create_base_keyboard, create_second_keyboard, create_date_keyboards, create_delivery_keyboards, create_confirmation_keyboard, create_size_keyboards
from helpers import parse_callback_data
import telebot
from telebot import TeleBot

current_dir = os.path.dirname(__file__)
user_data = {}


def handle_start(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        with open(f'{current_dir}/agreement.txt', 'rb') as file:
            bot.send_document(message.chat.id, file)
        bot.send_message(message.chat.id, "Для продолжения работы с ботом необходимо принять соглашение "
                                          "об обработке персональных данных."
                         " Прочтите соглашение и нажмите кнопку 'Принять'.",
                         reply_markup=create_consent_keyboard()
                         )
        print(f"Бот запущен пользователем: {message.chat.id}")


def handle_callbacks(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        try:
            chat_id = call.message.chat.id
            user_action = call.data
            if user_action == 'ok':
                bot.send_message(
                    call.message.chat.id,  "Спасибо! Вы приняли соглашение. Теперь вы можете продолжить.", reply_markup=create_base_keyboard())

            elif user_action == 'no':
                bot.send_message(call.message.chat.id,
                                 "Вы не приняли соглашение. Для продолжения работы с ботом необходимо дать согласие.")

            elif user_action.startswith("Бокс_"):
                box_name = parse_callback_data(user_action)[1]
                if chat_id not in user_data:
                    user_data[chat_id] = {}
                user_data[chat_id]['box'] = box_name
                bot.send_message(call.message.chat.id, f"""Вы выбрали: {
                                 user_data[chat_id]['box']}\nПожалуйста, выберите подходящий размер:
                                  Маленький: 1-3 м^3\nСредний:3-5 м^3\nБольшой: > 5м^3""", reply_markup=create_size_keyboards())
            elif user_action.startswith("date_"):
                box_date = parse_callback_data(user_action)[1]
                if chat_id not in user_data:
                    user_data[chat_id] = {}
                user_data[chat_id]['date'] = box_date
                bot.send_message(call.message.chat.id, f"""Вы выбрали дату: {
                                 user_data[chat_id]['date']}\nВыберите способ доставки: """, reply_markup=create_delivery_keyboards())

            elif user_action.startswith('delivery_'):
                box_delivery = parse_callback_data(user_action)[1]
                if chat_id not in user_data:
                    user_data[chat_id] = {}
                user_data[chat_id]['delivery'] = box_delivery
                bot.send_message(call.message.chat.id, f"""Вы выбрали доставку {
                                 user_data[chat_id]['delivery']}.\nПожлуйста, введите Имя получателя: """)
                bot.register_next_step_handler(
                    call.message, get_client_name, bot
                )
            elif user_action.startswith('confirmation_'):
                box_confirmation = parse_callback_data(user_action)[1]
                if chat_id not in user_data:
                    user_data[chat_id] = {}
                user_data[chat_id]['confirmation'] = box_confirmation
                bot.register_next_step_handler(
                    call.message, confirm_booking, bot)
            elif user_action == 'confirm_yes':
                bot.send_message(chat_id, "Бронирование подтверждено!")
            elif user_action == 'confirm_no':
                bot.send_message(chat_id, "Бронирование отклонено!")
            elif user_action.startswith('size_'):
                box_size = parse_callback_data(user_action)[1]
                if chat_id not in user_data:
                    user_data[chat_id] = {}
                user_data[chat_id]['size'] = box_size
                bot.send_message(call.message.chat.id, f"""Вы выбрали
                                 {user_data[chat_id]['size']} размер.\n Какая дата Вас инетересует?""", reply_markup=create_date_keyboards())

        except Exception as e:
            bot.send_message(call.message.chat.id,
                             f"Произошла ошибка. Повторите попытку позже. - {e}")


def handle_messages(bot: TeleBot):
    @bot.message_handler(func=lambda message: True)
    def handler_message(message):
        if message.text == "Цена":
            bot.send_message(
                message.chat.id, "Small: 120;\nMedium: 170;\nlarge: 200")
        elif message.text == "Заказать":
            bot.send_message(
                message.chat.id, "Пожалуйста, выберите подходящий Вам бокс: ", reply_markup=create_second_keyboard())
        elif message.text == "Мои Заказы":
            bot.send_message(
                message.chat.id, "Small: 120;\nMedium: 170;\nlarge: 200")
        elif message.text == "Правила Хранения":
            bot.send_message(
                message.chat.id, "Small: 120;\nMedium: 170;\nlarge: 200")


def get_client_name(message, bot):
    client_name = message.text.strip()
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]['name'] = client_name
    if message.text.strip().lower() in ['назад', 'отмена']:
        bot.send_message(
            message.chat.id,
            "Вы вернулись в главное меню.",
            reply_markup=create_base_keyboard()
        )
        return
    bot.send_message(
        message.chat.id, "Пожалуйста, укажите свой номер телефона:")
    bot.register_next_step_handler(
        message, get_client_number, bot)


def get_client_number(message, bot):
    client_number = message.text.strip()
    if message.chat.id in user_data:
        user_data[message.chat.id]['number'] = client_number

    if message.text.strip().lower() in ['назад', 'отмена']:
        bot.send_message(
            message.chat.id,
            "Вы вернулись в главное меню.",
            reply_markup=create_base_keyboard()
        )
        return
    confirm_booking_prompt(message, bot)


def get_client_main_info(message):
    user_info = user_data.get(message.chat.id, {})
    client_name = user_info.get('name', "none")
    client_number = user_info.get('number', "none")
    client_box = user_info.get('box', "none")
    client_date = user_info.get('date', "none")
    return client_name, client_number, client_box, client_date


def confirm_booking_prompt(message, bot):
    if message.text.strip().lower() in ['назад', 'отмена']:
        bot.send_message(
            message.chat.id,
            "Вы вернулись в главное меню.",
            reply_markup=create_base_keyboard()
        )
        return

    client_name, client_number, client_box, client_date = get_client_main_info(
        message)
    bot.send_message(message.chat.id,
                     f"Пожалуйста, подтвердите Ваш заказ:\n\n"
                     f"Бокс: {client_box}\n"
                     f"Имя: {client_name}\n"
                     f"День: {client_date}\n"
                     f"Номер: {client_number}\n",
                     reply_markup=create_confirmation_keyboard()
                     )


def confirm_booking(message, bot):
    user_response = message.text
    if user_response == "да":
        bot.send_message(
            message.chat.id,
            "Бронирование подтверждено!")
    else:
        bot.send_message(
            message.chat.id,
            "Бронирование отклонено!")
