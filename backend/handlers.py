import os
from datetime import datetime, timedelta
from datetime import datetime
from backend.models import StorageUser, StorageBox, Delivery, Order
from django.utils.timezone import now
from django.utils.timezone import make_aware


from inline_keyboards import (
    create_consent_keyboard,
    create_my_order_keyboard,
    create_box_info_keyboards,
    create_available_boxes_keyboard,
    create_delivery_keyboard,
    create_confirm_keyboard,
    go_back,
    show_details_2,

)
from standart_keyboards import (
    create_first_keyboard_user,
    create_second_keyboard_user,
    delivery_keybaord
)

import telebot
from django.db.models import Count


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
        from_user = call.from_user
        chat_id = call.message.chat.id
        user_action = call.data
        client, created = StorageUser.objects.get_or_create(
            tg_id=from_user.id,
            defaults={
                'name': from_user.first_name,
                'number': None,
                'role': 'customer'
            }
        )
        active_order = Order.objects.filter(
            user=StorageUser.objects.get(tg_id=chat_id)).first()

        if not client:
            client = StorageUser.objects.create(
                tg_id=from_user.id,
                name=from_user.first_name,
                number=None,
                role='customer'
            )

        def send_message(text, markup=None):
            bot.send_message(chat_id, text, reply_markup=markup)

        def edit_message_reply_markup(markup=None):
            bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=call.message.message_id,
                reply_markup=markup
            )

        if client:
            if user_action == 'accept':
                send_message(
                    "Спасибо! Вы приняли соглашение. Теперь вы можете продолжить.",
                    create_first_keyboard_user(client)
                )
            elif user_action == 'reject':
                send_message(
                    "Вы не приняли соглашение. Для продолжения работы с ботом необходимо дать согласие."
                )
            elif user_action == 'info_about_box':
                edit_message_reply_markup(create_box_info_keyboards())
            elif user_action == 'box_name':
                try:
                    storage_box = active_order.box
                    box = storage_box.name
                    if box:
                        send_message(
                            f'Название вашего бокса: {box}', go_back()
                        )
                except:
                    send_message(
                        "Вы еще не выбрали бокс 😓", go_back()
                    )
            elif user_action == 'box_end':
                if active_order:
                    active_order.status = 'Завершен'
                    active_order.rental_end_date = now()
                    active_order.is_notified = True
                    active_order.save()
                    storage_box = active_order.box
                    storage_box.available_from = now()
                    storage_box.save()
                    bot.send_photo(
                        chat_id,
                        photo=open(f"{current_dir}/qr_code.png", 'rb'),
                        caption=f"""Так быстро ??? Ваш заказ на бокс '{
                            storage_box.name}' завершен. Можете забрать по QR-коду"""
                    )
                else:
                    send_message("У вас нет активных заказов.", go_back())

            elif user_action == 'back':
                edit_message_reply_markup(create_box_info_keyboards())
            elif user_action == 'storage_period':
                try:
                    date_till = active_order.rental_end_date
                    rental_period = datetime.fromisoformat(
                        str(active_order.rental_end_date)).strftime("%Y-%m-%d")

                    send_message(
                        f"Период хранения:до {rental_period}", go_back()
                    )
                except:
                    send_message(
                        f"Период хранения:до 30 дней", go_back()
                    )
            elif user_action.startswith('available_'):
                box_name = user_action.split("_", 1)[1]
                chosen_box = StorageBox.objects.filter(name=box_name).first()
                if chosen_box:
                    user_data.setdefault(chat_id, {})['box_name'] = chosen_box
                    send_message(
                        f"""Вы выбрали {
                            chosen_box.name}\nНа сколько дней Вам нужна аренда?""",
                    )
                    bot.register_next_step_handler(
                        call.message, process_date, bot)
            elif user_action.startswith('delivery_'):
                box_delivery = user_action.split('_', 1)[1]
                user_data.setdefault(chat_id, {})[
                    'delivery_method'] = box_delivery
                if box_delivery == "курьером":
                    send_message(
                        "Отлично, Вы выбрали доставку: курьером\nЧто насчет Вашего адреса?"
                    )
                    bot.register_next_step_handler(
                        call.message, process_address, bot
                    )
                elif box_delivery == "самовывозом":
                    chosen_box = user_data[chat_id]['box_name']
                    user_data[chat_id]['client_address'] = chosen_box.location
                    send_message(
                        f"""Адрес вашего бокса: {
                            chosen_box.location}\nМы почти у цели!!\n\nУкажите имя получателя:"""
                    )
                    bot.register_next_step_handler(
                        call.message, process_name, bot
                    )
            elif user_action.startswith('confirm_'):
                response = user_action.split('_', 1)[1]
                if response == 'accept':
                    confirm_booking(call.message, bot)
                else:
                    send_message(
                        "Дубль №2", create_first_keyboard_user(client)
                    )
            elif user_action == 'all_orders':
                boxes = client.property.all()
                orders = Order.objects.filter(
                    box__in=boxes).select_related('user', 'box')
                order_details = []

                for order in orders:
                    created_at_str = (
                        datetime.fromisoformat(
                            str(order.created_at)).strftime('%d.%m.%Y %H:%M')
                        if order.created_at else 'Не указано'
                    )

                    rental_end_date_str = (
                        order.rental_end_date.strftime('%d.%m.%Y %H:%M')
                        if order.rental_end_date else 'Не указано'
                    )

                    order_details.append(
                        f"Заказ #{order.id}:\n"
                        f"Клиент: {order.user.name} (ID: {order.user.tg_id})\n"
                        f"Склад: {order.box.name}\n"
                        f"Статус: {order.status}\n"
                        f"Описание вещей: {order.items_description}\n"
                        f"Создан: {created_at_str}\n"
                        f"Срок: до {rental_end_date_str}\n"
                        "-----------------------------------"
                    )
                details_message = "\n\n".join(order_details)
                send_message(details_message)
            elif user_action == 'end_orders':
                boxes = client.property.all()
                orders = Order.objects.filter(
                    box__in=boxes,
                    status="Задержка"
                ).select_related('user', 'box')

                if orders.exists():
                    order_details = []
                    for order in orders:
                        order_details.append(
                            f"Заказ #{order.id}:\n"
                            f"""Клиент: {order.user.name} (ID: {
                                order.user.tg_id})\n"""
                            f"Склад: {order.box.name}\n"
                            f"Статус: {order.status}\n"
                            f"Описание вещей: {order.items_description}\n"
                            f"""Закончился: {
                                order.rental_end_date.strftime('%d.%m.%Y %H:%M')}\n"""
                            f"""Доступен с: {
                                order.box.available_from.strftime('%d.%m.%Y %H:%M')}\n"""
                            "-----------------------------------"
                        )
                    send_message("\n\n".join(order_details))
                else:
                    send_message("Нет просроченных заказов.")

        else:
            send_message("Пользователь не найден.")


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
            if boxes:
                box_info = []
                for box in boxes:
                    time_from = box.available_from.strftime("%d.%m.%Y")
                    time_till = box.available_till.strftime("%d.%m.%Y")
                    box_details = f"Бокс: {box.name}\n\n"
    
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
            else:
                bot.send_message(
                    message.chat.id, "На данный момент доступных боксов нет.")

        elif message.text == "Просмотреть заказы":
            boxes = client.property.all()
            orders = Order.objects.filter(
                box__in=boxes).select_related('user', 'box')
            if orders.exists():
                total_orders = orders.count()
                bot.send_message(
                    message.chat.id,
                    f"Всего заказов для ваших складов: {total_orders}", reply_markup=show_details_2()
                )
        elif message.text == "Управление боксами":
            boxes = client.property.all()
            if boxes.exists():
                box_list = "\n".join(
                    [f"{box.name} (ID: {box.id})" for box in boxes])
                bot.send_message(message.chat.id, f"""Ваши боксы:\n{
                                 box_list}""", reply_markup=delivery_keybaord())
            else:
                bot.send_message(
                    message.chat.id, "У вас нет зарегистрированных боксов.", reply_markup=delivery_keybaord())

        elif message.text.startswith("Доставка Заказа"):
            print(f"Client tg_id: {client}")
            deliveries = Delivery.objects.filter(
                order__box__owners__tg_id=client.tg_id
            ).select_related('order__user', 'order__box')
            print(f"Queryset count: {deliveries.count()}")
            if deliveries.exists():
                all_deliveries = "\n\n".join(
                    [
                        f"Заказ ID: {delivery.order.id}\n"
                        f"Адрес получения: {delivery.pickup_address}\n"
                        f"Контактный номер: {delivery.contact_number}\n"
                        f"""Назначенная дата: {
                            delivery.scheduled_at.strftime('%d.%m.%Y %H:%M')}"""
                        for delivery in deliveries
                    ]
                )

                bot.send_message(
                    message.chat.id,
                    f"Найденные доставки:\n\n{all_deliveries}\n\n"
                )
            else:
                bot.send_message(
                    message.chat.id, "Доставка не найдена или не принадлежит вашему боксу."
                )


def process_delivery(message, bot):
    try:
        order_id = int(message.text.strip())
        delivery = Delivery.objects.filter(
            order__id=order_id,
            order__box__owners__tg_id=message.chat.id
        ).select_related('order__user', 'order__box').first()

        if delivery:
            pickup_address = delivery.pickup_address
            contact_number = delivery.contact_number
            scheduled_date = delivery.scheduled_at.strftime("%d.%m.%Y %H:%M")

            bot.send_message(
                message.chat.id,
                f"Доставка для заказа #{delivery.order.id}\n"
                f"Адрес получения: {pickup_address}\n"
                f"Контактный номер: {contact_number}\n"
                f"Назначенная дата: {scheduled_date}"
            )
        else:
            bot.send_message(
                message.chat.id,
                "Доставка не найдена или заказ указан неверно. Попробуйте еще раз, указав ID заказа."
            )
            bot.register_next_step_handler(message, process_delivery, bot)
    except ValueError:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, введите корректный ID заказа (число)."
        )
        bot.register_next_step_handler(message, process_delivery, bot)
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"Произошла ошибка: {str(e)}. Попробуйте снова."
        )


def process_date(message, bot):
    chat_id = message.chat.id
    user_input = message.text.strip()

    try:
        rental_days = int(user_input)
        if rental_days <= 0:
            bot.send_message(
                chat_id, "Пожалуйста, введите положительное число дней.")
            bot.register_next_step_handler(message, process_date, bot)
            return
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректное число дней.")
        bot.register_next_step_handler(message, process_date, bot)
        return

    chosen_box = user_data.get(chat_id, {}).get('box_name')
    if not chosen_box:
        bot.send_message(chat_id, "Что-то пошло не так, выберите бокс заново.")
        return

    now = make_aware(datetime.now())
    rental_end_date = now + timedelta(days=rental_days)

    if rental_end_date > chosen_box.available_till:
        bot.send_message(
            chat_id,
            f"Извините, выбранный период аренды выходит за пределы доступного времени для этого бокса. "
            f"""Максимально доступный срок аренды: {(
                chosen_box.available_till - now).days} дней. Пожалуйста, выберите более короткий срок."""
        )
        bot.register_next_step_handler(message, process_date, bot)
        return

    user_data[chat_id]['rental_date'] = rental_end_date
    bot.send_message(
        chat_id,
        f"{rental_days} так {rental_days}!\nЧто насчет способа доставки?",
        reply_markup=create_delivery_keyboard()
    )


def process_user_input(message, bot, next_step_handler, key, prompt):
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id][key] = message.text.strip()
    bot.send_message(message.chat.id, prompt)
    bot.register_next_step_handler(message, next_step_handler, bot)


def process_address(message, bot):
    process_user_input(message, bot, process_name, 'client_address',
                       "Почти у цели!\nУкажите Имя получателя:")


def process_name(message, bot):
    process_user_input(message, bot, confirm_request, 'client_name',
                       "Осталось всего 2 шага!!\nУкажите Контактный номер телефона получателя:")


def get_main_info_about_user(message):
    user_info = user_data.get(message.chat.id, {})
    client_name = user_info.get("client_name", "no")
    client_phone = user_info.get("client_phone", "no")
    client_box = user_info.get("box_name", "no")
    client_address = user_info.get("client_address", "no")
    client_date = user_info.get('rental_date', 'no')
    return client_name, client_phone, client_box, client_address, client_date


def confirm_request(message, bot):
    client_phone = message.text.strip()
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]['client_phone'] = client_phone
    client = StorageUser.objects.filter(tg_id=message.chat.id).first()

    if client:
        client.number = client_phone
        client.rental_period = user_data[message.chat.id].get('rental_date')
        client.save()

    client_name, client_phone, client_box, client_address, client_date = get_main_info_about_user(
        message)

    formatted_date = datetime.fromisoformat(
        str(client_date)).strftime("%Y-%m-%d")
    bot.send_message(
        message.chat.id,
        "Cупер!!\nОсталось только подтвердить и собрать Ваши вещи к хранению!",
    )
    bot.send_message(
        message.chat.id,
        f"Пожалуйста, подтвердите бронирование:\n"
        f"Выбранный бокс: {client_box}\n"
        f"Период: до {formatted_date}\n"
        f"Имя клиента: {client_name}\n"
        f"Телефон: {client_phone}\n"
        f"Адрес: {client_address}\n",
        reply_markup=create_confirm_keyboard(),
    )


def finish_rent(message, bot):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    chosen_box = user_data.get(chat_id, {}).get('box_name')
    order = Order.objects.filter(
        rental_end_date__isnull=False, is_notified=False, user=user_name)
    order.rental_end_date = chosen_box.available_till
    order.is_notified = True
    order.save()
    bot.send_photo(
        order.user.tg_id,
        photo=open(f"{current_dir}/qr_code.png", 'rb'),
        caption=f"""Привет, {
            order.user.name}!\nВремя так быстро летит((\n Срок твоей аренды уже закончился\nВот QR-код, чтобы забрать свои вещи 😓 📷\n\nPS.Мы будем скучать!"""
    )


def confirm_booking(message, bot):
    chat_id = message.chat.id

    if chat_id not in user_data:
        bot.send_message(chat_id, "Что-то пошло не так. Попробуйте снова.")
        return
    try:
        chosen_box = user_data[chat_id]['box_name']
        delivery_method = user_data[chat_id]['delivery_method']
        client_address = user_data[chat_id].get('client_address', '')
        rental_date = user_data[chat_id].get('rental_date', '')
        user_name = user_data[chat_id].get(
            'name', message.from_user.first_name)

        # Здесь сохраняем ордер
        client = StorageUser.objects.get(tg_id=chat_id)
        order = Order.objects.create(
            user=client,
            box=chosen_box,
            status='Обрабатывается',
            items_description=f"""Заказ от <<{user_data[chat_id]['client_name']}>> на бокс <<{
                chosen_box.name}>> с доставкой <<{delivery_method}>> по адресу <<{client_address}>>""",
            rental_end_date=rental_date
        )

        if delivery_method == 'курьером':
            Delivery.objects.create(
                order=order,
                pickup_address=client_address,
                contact_number=client.number,
                scheduled_at=datetime.now(),
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
            caption="""Вот ваш QR-код 📷\nОн нужен, чтобы открыть Вашу ячейку для хранения вещей\n\nКак срок аренды подойдет к концу, Вы получите другой QR-код для доступа. \nУдачи!)"""
        )
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка при оформлении заказа: {str(e)}")
