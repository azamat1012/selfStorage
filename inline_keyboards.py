import telebot


# def create_back_buttom():
#     return telebot.types.KeyboardButton('Назад')


def create_my_order_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    info_botton = telebot.types.InlineKeyboardButton(
        'Иформация об арендуемом боксе',
        callback_data='info_about_box'
    )
    keyboard.add(info_botton)

    return keyboard


def create_box_info_keyboards():
    keyboard = telebot.types.InlineKeyboardMarkup()
    storage_period_button = telebot.types.InlineKeyboardButton(
        'Период хранения',
        callback_data='storage_period'
    )
    box_name_button = telebot.types.InlineKeyboardButton(
        'Название бокса',
        callback_data='box_name'
    )
    keyboard.add(storage_period_button)
    keyboard.add(box_name_button)

    return keyboard


def create_consent_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    accept_buttom = telebot.types.InlineKeyboardButton(
        "Принять",
        callback_data='accept'
        )
    reject_buttom = telebot.types.InlineKeyboardButton(
        "Отклонить",
        callback_data='reject')
    keyboard.add(accept_buttom, reject_buttom)

    return keyboard


