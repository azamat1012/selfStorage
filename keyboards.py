import telebot


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
