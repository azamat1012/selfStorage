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


# def create_first_keyboard_user():
#     keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button_1 = telebot.types.KeyboardButton("Заказать бокс для вещей")
#     button_2 = telebot.types.KeyboardButton("Я владелец.")

#     keyboard.row(button_1, button_2)
#     return keyboard


# def create_second_keyboard_user():
#     keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button_3 = telebot.types.KeyboardButton('Прайс')
#     button_4 = telebot.types.KeyboardButton('Оформить заказ')
#     button_5 = telebot.types.KeyboardButton('Мои заказы')
#     button_6 = telebot.types.KeyboardButton('Правила хранения')
#     back_botton = create_back_buttom()
#     keyboard.row(button_3, button_6)
#     keyboard.row(button_4, button_5)
#     keyboard.row(back_botton)

    return keyboard