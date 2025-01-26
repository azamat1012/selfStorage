import os
from datetime import datetime
from backend.models import StorageUser, StorageBox, Delivery, Order
import telebot

from inline_keyboards import (
    create_consent_keyboard,
    create_my_order_keyboard,
    create_box_info_keyboards,
    create_available_boxes_keyboard,
    create_delivery_keyboard,
    create_confirm_keyboard,
    go_back
)
from standart_keyboards import (
    create_first_keyboard_user,
    create_second_keyboard_user,
    create_third_keyboard_user,
)


user_data = {}
current_dir = os.path.dirname(__file__)

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def handle_start(bot: telebot.TeleBot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        with open('agreement.txt', 'rb') as file:
            bot.send_document(message.chat.id, file)
        bot.send_message(
            message.chat.id,
            "Для продолжения работы с ботом необходимо принять соглашение "
            "об обработке персональных данных. Прочтите соглашение и нажмите кнопку 'Принять'.",
            reply_markup=create_consent_keyboard()
        )


def handle_callbacks(bot: telebot.TeleBot):

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        print("Telegram ID:", call.from_user.id)
        client = StorageUser.objects.filter(tg_id=call.from_user.id).first()
        chat_id = call.message.chat.id
        user_action = call.data
        user_address = call.message.chat.id
        if not client:
            client = StorageUser.objects.create(
                tg_id=call.from_user.id,
                name=call.from_user.first_name,
                number=None,
                role='customer'
            )

        if client:
            if user_action == 'accept':
                bot.send_message(
                    user_address,
                    "Спасибо! Вы приняли соглашение. Теперь вы можете продолжить.",
                    reply_markup=create_first_keyboard_user(client)
                )
                print(client)
            elif user_action == 'reject':
                bot.send_message(
                    user_address,
                    "Вы не приняли соглашение. Для продолжения работы с ботом необходимо дать согласие."
                )
            elif user_action == 'info_about_box':
                bot.edit_message_reply_markup(
                    chat_id=user_address,
                    message_id=call.message.message_id,
                    reply_markup=create_box_info_keyboards()
                )
            elif user_action == 'box_name':
                try:
                    box = user_data[chat_id]['box_name']

                    bot.send_message(user_address,
                                     f'Название вашего бокса: {box}', reply_markup=go_back())
                except Exception as e:
                    bot.send_message(
                        user_address, "Вы еще не выбрали бокс 😓", reply_markup=go_back())

            elif user_action == "back":
                bot.edit_message_reply_markup(
                    chat_id=user_address,
                    message_id=call.message.message_id,
                    reply_markup=create_box_info_keyboards()
                )

            elif user_action == 'storage_period':
                bot.send_message(
                    user_address, "Период хранения: 30 дней", reply_markup=go_back())

            elif user_action.startswith('available_'):
                box_name = user_action.split("_", 1)[1]
                chosen_box = StorageBox.objects.filter(name=box_name).first()
                if chosen_box:
                    if chat_id not in user_data:
                        user_data[chat_id] = {}
                    user_data[chat_id]['box_name'] = chosen_box
                bot.send_message(user_address,
                                 f"Вы выбрали {chosen_box.name}\nКакой способ доставки Вас интересует?", reply_markup=create_delivery_keyboard())

            elif user_action.startswith('delivery_'):
                box_delivery = user_action.split('_', 1)[1]
                if box_delivery == "курьером":
                    if chat_id not in user_data:
                        user_data[chat_id] = {}
                    user_data[chat_id]['delivery_method'] = box_delivery
                    bot.send_message(
                        user_address, f"Отлично, Вы выбрали доставку: курьером\nЧто насчет Вашего адреса?")
                    bot.register_next_step_handler(
                        call.message, process_address, bot)

                elif box_delivery == "самовывозом":
                    if chat_id not in user_data:
                        user_data[chat_id] = {}
                    user_data[chat_id]['delivery_method'] = box_delivery
                    chosen_box = user_data[chat_id]['box_name']
                    user_data[chat_id]['client_address'] = chosen_box.location
                    bot.send_message(user_address, f"""Адрес вашего бокса: {
                                     chosen_box.location}\nМы почти у цели!!\n\nУкажите имя получателя:""")
                    bot.register_next_step_handler(
                        call.message, process_name, bot)
            elif user_action.startswith('confirm_'):
                response = user_action.split('_', 1)[1]
                if response == 'accept':
                    confirm_booking(call.message, bot)
                else:
                    bot.send_message(user_address, "Дубль №2",
                                     reply_markup=create_first_keyboard_user())

        else:
            bot.send_message(call.message.chat.id, "Пользователь не найден.")


def process_address(message, bot):
    client_address = message.text
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]['client_address'] = client_address
    bot.send_message(message.chat.id, "Почти у цели!\nУкажите Имя получателя:")
    bot.register_next_step_handler(message, process_name, bot)


def process_name(message, bot):
    client_name = message.text.strip()
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]['client_name'] = client_name

    bot.send_message(
        message.chat.id, "Осталось всего 2 шага!!\nУкажите Контактный номер телефона получателя:")
    bot.register_next_step_handler(message, confirm_request, bot)


def get_main_info_about_user(message):
    user_info = user_data.get(message.chat.id, {})
    client_name = user_info.get("client_name", "no")
    client_phone = user_info.get("client_phone", "no")
    client_box = user_info.get("box_name", "no")
    client_address = user_info.get("client_address", "no")
    return client_name, client_phone, client_box, client_address


def confirm_request(message, bot):
    client_phone = message.text.strip()
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]['client_phone'] = client_phone
    client_name, client_phone, client_box, client_address = get_main_info_about_user(
        message)
    bot.send_message(
        message.chat.id, "Cупер!!\nОсталось только подтвердить и собрать Ваши вещи к хранению храненяю",)

    bot.send_message(message.chat.id,
                     f"Пожалуйста, подтвердите бронирование:\n"
                     f"Имя клиента: {client_name}\n"
                     f"Телефон: {client_phone}\n"
                     f"Выбранный бокс: {client_box}\n"
                     f"Адрес: {client_address}\n",
                     reply_markup=create_confirm_keyboard())


def confirm_booking(message, bot):
    chat_id = message.chat.id

    if chat_id not in user_data:
        bot.send_message(chat_id, "Что-то пошло не так. Попробуйте снова.")
        return
    try:
        chosen_box = user_data[chat_id]['box_name']
        delivery_method = user_data[chat_id]['delivery_method']
        client_address = user_data[chat_id].get('client_address', '')
        user_name = user_data[chat_id].get(
            'name', message.from_user.first_name)

        # Здесь сохраняем ордер
        client = StorageUser.objects.get(tg_id=chat_id)
        order = Order.objects.create(
            user=client,
            box=chosen_box,
            status='pending',
            items_description=f"Заказ на бокс {
                chosen_box.name} с доставкой {delivery_method}",
        )

        if delivery_method == 'delivery_курьером':
            Delivery.objects.create(
                order=order,
                pickup_address=client_address,
                contact_number=client.number,
                scheduled_at=datetime.now(),
                delivery_method=delivery_method,
            )

        bot.send_message(
            chat_id,
            f"Ваш заказ успешно оформлен! 🏷️\n"
            f"Бокс: {chosen_box.name}\n"
            f"Метод получения: {delivery_method}\n"
            f"Статус заказа: {order.get_status_display()}",
            reply_markup=create_second_keyboard_user(client)
        )
        bot.send_photo(
            chat_id,
            photo=open(f"{current_dir}/qr_code.png", 'rb'),
            caption="Вот ваш QR-код 📷"
        )
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка при оформлении заказа: {str(e)}")


def handle_messages(bot: telebot.TeleBot):
    @bot.message_handler(func=lambda message: True)
    def handler_message(message):
        client = StorageUser.objects.filter(tg_id=message.from_user.id).first()
        if not client:
            client = StorageUser.objects.create(
                tg_id=message.from_user.id,
                name=message.from_user.first_name,
                number=None,
                role='customer'
            )
        if message.text == 'Заказать бокс для вещей':
            bot.send_message(
                message.chat.id,
                'Спасибо, что выбрали нас.',
                reply_markup=create_second_keyboard_user(client)
            )
        elif message.text == 'Прайс':
            bot.send_message(message.chat.id, read_file('price.txt'))
        elif message.text == 'Назад':
            bot.send_message(
                message.chat.id,
                'Возвращаемся в Главное меню',
                reply_markup=create_first_keyboard_user(client)
            )
        elif message.text == 'Правила хранения':
            bot.send_message(message.chat.id, read_file('storage_rules.txt'))
        elif message.text == 'Мои заказы':
            bot.send_message(
                message.chat.id,
                'Выберите действие',
                reply_markup=create_my_order_keyboard()
            )
        elif message.text == 'Оформить заказ':

            boxes = StorageBox.objects.all()
            box_info = []
            for box in boxes:
                time_from = box.available_from.strftime("%d.%m.%Y")
                time_till = box.available_till.strftime("%d.%m.%Y")
                box_details = f"-----------Бокс: {box.name}-----------\n\n"

                box_details += f"Описание: {box.description}\n\n"
                box_details += f"Цена: {box.price} руб.\n\n"
                box_details += f"Площадь: {box.volume}\n\n"
                box_details += f"""Время работы: {
                    time_from} - {time_till} \n\n"""
                box_details += f"Адрес: {box.location} \n\n"
                box_info.append(box_details)

            box_info_message = "Доступные боксы:\n\n" + "\n".join(box_info)
            bot.send_message(message.chat.id, box_info_message)
            bot.send_message(
                message.chat.id,
                'Выберите бокс из доступных',
                reply_markup=create_available_boxes_keyboard()
            )
