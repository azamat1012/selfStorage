import django
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def create_consent_keyboard():
    keyboard = InlineKeyboardMarkup()
    accept_button = InlineKeyboardButton(
        'OK', callback_data='ok'
    )
    reject_button = InlineKeyboardButton(
        'NO', callback_data='no'
    )
    keyboard.add(accept_button, reject_button)
    return keyboard


def create_base_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Цена")
    button2 = KeyboardButton("Заказать")
    button3 = KeyboardButton("Мои Заказы")
    button4 = KeyboardButton("Правила Хранения")
    keyboard.row(button1, button2)
    keyboard.row(button3, button4)
    return keyboard


def create_second_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(
        "Бокс Белая поляна", callback_data="Бокс_Белая поляна")
    button2 = InlineKeyboardButton(
        "Бокс Красная поляна", callback_data="Бокс_Красная поляна")
    button3 = InlineKeyboardButton(
        "Бокс Желтая поляна", callback_data="Бокс_Желтая поляна")
    button4 = InlineKeyboardButton(
        "Бокс Зеленая поляна", callback_data="Бокс_Зеленая поляна")
    keyboard.add(button1, button2, button3, button4)
    return keyboard


def create_date_keyboards():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(
        "Понедельник", callback_data="date_Понедельник")
    button2 = InlineKeyboardButton("Вторник", callback_data="date_Вторник")
    button3 = InlineKeyboardButton("Среда", callback_data="date_Среда")
    button4 = InlineKeyboardButton("Четверг", callback_data="date_Четверг")
    button5 = InlineKeyboardButton("Пятница", callback_data="date_Пятница")
    button6 = InlineKeyboardButton("Суббота", callback_data="date_Суббота")
    button7 = InlineKeyboardButton(
        "Воскресенье", callback_data="date_Воскресенье")
    keyboard.add(button1, button2, button3, button4, button5, button6, button7)
    return keyboard


def create_delivery_keyboards():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(
        "Самовывоз", callback_data="delivery_самовывозом")
    button2 = InlineKeyboardButton(
        "Курьер до дома", callback_data="delivery_курьером")
    keyboard.add(button1, button2)
    return keyboard


def create_confirmation_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(
        "Да", callback_data="confirm_yes")
    button2 = InlineKeyboardButton(
        "Нет", callback_data="confirm_no")
    keyboard.add(button1, button2)
    return keyboard


def create_size_keyboards():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(
        "Маленький", callback_data="size_small")
    button2 = InlineKeyboardButton("Средний", callback_data="size_medium")
    button3 = InlineKeyboardButton("Большой", callback_data="size_big")
    button4 = InlineKeyboardButton("Цена", callback_data=" Цена")

    keyboard.add(button1, button2, button3, button4)
    return keyboard
