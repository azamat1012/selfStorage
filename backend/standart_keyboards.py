from backend.models import StorageUser
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def create_back_button():
    return KeyboardButton('Назад')


def create_first_keyboard_user(client):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if client.role == 'customer':
        button_1 = KeyboardButton("Заказать бокс для вещей")
        button_2 = KeyboardButton("Правила хранения")
        keyboard.row(button_1)
        keyboard.row(button_2)
    elif client.role == 'staff':
        button_1 = KeyboardButton("Просмотреть заказы")
        button_2 = KeyboardButton("Управление боксами")
        keyboard.row(button_1)
        keyboard.row(button_2)

    return keyboard


def create_second_keyboard_user(client):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if client.role == 'customer':
        button_3 = KeyboardButton('Прайс')
        button_4 = KeyboardButton('Оформить заказ')
        button_5 = KeyboardButton('Мои заказы')
        button_6 = KeyboardButton('Правила хранения')
        back_button = create_back_button()

        keyboard.row(button_3, button_6)
        keyboard.row(button_4, button_5)
        keyboard.row(back_button)
    return keyboard


def create_fourth_keyboard_user():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton('Посмотреть мои боксы')
    back_button = create_back_button()
    keyboard.row(back_button, button1)
    return keyboard


def delivery_keybaord():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Доставка Заказа")
    back_button = create_back_button()
    keyboard.row(button, back_button)
    return keyboard
