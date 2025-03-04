import asyncio
import httpx
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from datetime import datetime


import bot.keyboard as kb
from app.config import settings


current_date = datetime.now().strftime("%d.%m.%Y")
bot = Bot(settings.TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_bot(message: Message):
    await message.reply('Hello', reply_markup=kb.main)

@dp.message(F.text == 'Today matches')
async def events(message: Message):
    async with httpx.AsyncClient() as client:
        result = await client.get('http://127.0.0.1:8000/events')
    mes = f'Today:  {current_date}'
    for i in result.json().get('today_events'):
        mes += f'\n { i['time']}:   {i['owner']}  -  {i['guest']}'
    await message.answer(mes)

async def main():
    print("Бот запущен. Ожидаем задачи...")
    await dp.start_polling(bot)



if __name__ == '__main__':

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')