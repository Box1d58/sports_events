from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обновить данные')]
],
    resize_keyboard=True,
    input_field_placeholder='Выбери')

upgrade_info = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сегодняшние матчи')]
],
    resize_keyboard=True,
    input_field_placeholder='Выбери')