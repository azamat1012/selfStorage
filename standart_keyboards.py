import telebot


def create_back_buttom():
    return telebot.types.KeyboardButton('Назад')


def create_first_keyboard_user():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = telebot.types.KeyboardButton("Заказать бокс для вещей")
    button_2 = telebot.types.KeyboardButton("Я владелец")

    keyboard.row(button_1, button_2)
    return keyboard


def create_second_keyboard_user():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_3 = telebot.types.KeyboardButton('Прайс')
    button_4 = telebot.types.KeyboardButton('Оформить заказ')
    button_5 = telebot.types.KeyboardButton('Мои заказы')
    button_6 = telebot.types.KeyboardButton('Правила хранения')
    back_botton = create_back_buttom()
    keyboard.row(button_3, button_6)
    keyboard.row(button_4, button_5)
    keyboard.row(back_botton)

    return keyboard


def create_third_keyboard_user():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_7 = telebot.types.KeyboardButton('Посмотреть доступные боксы')
    back_botton = create_back_buttom()
    keyboard.row(button_7)
    keyboard.row(back_botton)

    return keyboard


def create_fourth_keyboard_user():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_8 = telebot.types.KeyboardButton('Самовывоз')
    button_9 = telebot.types.KeyboardButton('Заказ курьера')
    back_botton = create_back_buttom()
    keyboard.add(button_8, button_9)
    keyboard.row(back_botton)

    return keyboard

def create_first_keyboard_owner():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = telebot.types.KeyboardButton('Статистика')
    button_2 = telebot.types.KeyboardButton('Создать бокс')

    keyboard.add(button_1, button_2)
    return keyboard
