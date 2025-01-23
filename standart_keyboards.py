import telebot


def create_back_buttom():
    return telebot.types.KeyboardButton('Назад')


def create_first_keyboard_user():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = telebot.types.KeyboardButton("Заказать бокс для вещей")
    button_2 = telebot.types.KeyboardButton("Я владелец.")

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
