import telebot


def create_back_buttom():
    return telebot.types.KeyboardButton('Назад')


def create_consent_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    accept_buttom = telebot.types.InlineKeyboardButton(
        "Принять",
        callback_data='aacept'
        )
    reject_buttom = telebot.types.InlineKeyboardButton(
        "Отклонить",
        callback_data='reject')
    keyboard.add(accept_buttom, reject_buttom)

    return keyboard


def create_first_keybords():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = telebot.types.KeyboardButton("Я хочу заказать у вас бокс для вещей.")
    button_2 = telebot.types.KeyboardButton("Я владелец.")

    keyboard.row(button_1, button_2)