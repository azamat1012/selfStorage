from datetime import datetime
from django.utils.timezone import now
from backend.models import Order
import os
import telebot
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('TG_BOT_TOKEN'))
current_dir = os.path.dirname(__file__)


def notify_users():
    orders = Order.objects.filter(
        rental_end_date__isnull=False, is_notified=False)
    print(f"Orders to notify: {orders.count()}")

    for order in orders:
        time_left = order.rental_end_date - now()
        days_left = time_left.days
        formatted_date = order.rental_end_date.strftime("%Y-%m-%d")

        if days_left in [3, 5, 15]:
            message = f"""Привет, {order.user.name}!\nХотим напомнить, что твоя аренда на бокс '{
                order.box.name}' до '{formatted_date}'. \nНе забудь :)"""
            bot.send_message(order.user.tg_id, message)
            order.save()
            print(f"Уведомление отправлено {order.user.name}")
        if 0 <= days_left <= 1:
            bot.send_photo(
                order.user.tg_id,
                photo=open(f"{current_dir}/qr_code.png", 'rb'),
                caption=f"""Привет, {
                    order.user.name}!\nВремя так быстро летит((\n Срок твоей аренды уже закончился\nВот QR-код, чтобы забрать свои вещи 😓 \n\nPS.Мы будем скучать!"""
            )
        if days_left < 0:
            bot.send_photo(
                order.user.tg_id,
                photo=open(f"{current_dir}/qr_code.png", 'rb'),
                caption=f"""Привет, {
                    order.user.name}!!!\nМы конечно, все понимаем, но срок уже истек, соответсвенно тарифный план за хранение нам придется увелчить\nВот QR-код, чтобы забрать свои вещи 😓 \n\nPS.Мы будем скучать!"""
            )
