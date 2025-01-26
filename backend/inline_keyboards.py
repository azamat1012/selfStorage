from backend.models import StorageBox
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_my_order_keyboard():
    keyboard = InlineKeyboardMarkup()
    info_button = InlineKeyboardButton(
        'Информация об арендуемом боксе',
        callback_data='info_about_box'
    )
    keyboard.add(info_button)
    return keyboard


def create_box_info_keyboards():
    keyboard = InlineKeyboardMarkup()
    storage_period_button = InlineKeyboardButton(
        'Период хранения',
        callback_data='storage_period'
    )
    box_name_button = InlineKeyboardButton(
        'Название бокса',
        callback_data='box_name'
    )
    keyboard.add(storage_period_button)
    keyboard.add(box_name_button)
    return keyboard


def create_consent_keyboard():
    keyboard = InlineKeyboardMarkup()
    accept_button = InlineKeyboardButton(
        "Принять",
        callback_data='accept'
    )
    reject_button = telebot.types.InlineKeyboardButton(
        "Отклонить",
        callback_data='reject'
    )
    keyboard.add(accept_button, reject_button)
    return keyboard


def create_available_boxes_keyboard():
    keyboard = InlineKeyboardMarkup()
    boxes = StorageBox.objects.all()
    for box in boxes:
        button = InlineKeyboardButton(
            box.name, callback_data=f"available_{box.name}")
        keyboard.add(button)
    return keyboard


def create_delivery_keyboard():
    keyboard = InlineKeyboardMarkup()
    button_self = InlineKeyboardButton(
        'Самовывоз', callback_data='delivery_самовывозом')
    button_curier = InlineKeyboardButton(
        'Заказ курьера', callback_data='delivery_курьером')
    keyboard.add(button_self, button_curier)
    return keyboard


def create_confirm_keyboard():

    keyboard = InlineKeyboardMarkup()
    accept_button = InlineKeyboardButton(
        "OK",
        callback_data='confirm_accept'
    )
    reject_button = InlineKeyboardButton(
        "Не ок",
        callback_data='confirm_reject'
    )
    keyboard.add(accept_button, reject_button)
    return keyboard


def go_back():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        "Назад",
        callback_data='back'
    )
    keyboard.add(button)
    return keyboard
