from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import callback_data
from app.config import settings

upgrade_info = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Сегодняшние матчи'), KeyboardButton(text='Выбрать команду')]
],
    resize_keyboard=True,
    input_field_placeholder='Выбери')

upgrade = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔄 Обновить информацию', callback_data='upgrade_info')]
])