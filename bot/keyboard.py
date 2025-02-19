from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Today matches')]
],
    resize_keyboard=True,
    input_field_placeholder='Choose')