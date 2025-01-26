from backend.models import StorageUser
import telebot


def create_back_button():
    return telebot.types.KeyboardButton('Назад')


def create_first_keyboard_user(client):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if client.role == 'customer':
        button_1 = telebot.types.KeyboardButton("Заказать бокс для вещей")
        button_2 = telebot.types.KeyboardButton("Правила хранения")
        keyboard.row(button_1)
        keyboard.row(button_2)
    elif client.role == 'staff':
        button_1 = telebot.types.KeyboardButton("Просмотреть заказы")
        button_2 = telebot.types.KeyboardButton("Управление боксами")
        keyboard.row(button_1)
        keyboard.row(button_2)

    return keyboard


def create_second_keyboard_user(client):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if client.role == 'customer':
        button_3 = telebot.types.KeyboardButton('Прайс')
        button_4 = telebot.types.KeyboardButton('Оформить заказ')
        button_5 = telebot.types.KeyboardButton('Мои заказы')
        button_6 = telebot.types.KeyboardButton('Правила хранения')
        back_button = create_back_button()

        keyboard.row(button_3, button_6)
        keyboard.row(button_4, button_5)
        keyboard.row(back_button)
    return keyboard


def create_third_keyboard_user(client):

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    if client.role == 'customer':
        button_7 = telebot.types.KeyboardButton('Посмотреть доступные боксы')
        back_button = create_back_button()
        keyboard.row(button_7)
        keyboard.row(back_button)
    elif client.role == 'staff':
        button_7 = telebot.types.KeyboardButton('Добавить новый бокс')
        button_8 = telebot.types.KeyboardButton('Удалить бокс')
        back_button = create_back_button()
        keyboard.row(button_7, button_8)
        keyboard.row(back_button)

    return keyboard


def create_fourth_keyboard_user():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Посмотреть мои боксы')
    back_button = create_back_button()
    keyboard.row(back_button, button1)
    return keyboard
