import asyncio
import httpx
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from datetime import datetime


import bot.keyboard as kb
from app.config import settings
from app.database import async_session_maker
from app.models_db import TeamsDB

logging.basicConfig(level=logging.INFO)

current_date = datetime.now().strftime("%d.%m.%Y")
bot = Bot(settings.TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_bot(message: Message):
    await message.reply('Привет, я телеграм бот, которые умеет показывать сегодняшние матчи КХЛ'
                        , reply_markup=kb.start)

@dp.message(F.text == 'Сегодняшние матчи')
async def events(message: Message):
    logging.info(message.from_user.username)
    logging.info(message.from_user.id)
    async with httpx.AsyncClient() as client:
        result = await client.get('http://127.0.0.1:8000/events')
    mes = f'Сегодняшняя дата:  {current_date}'
    mes += f'\n------------------------------'
    for i in result.json().get('today_events'):
        async with async_session_maker() as session:
            i['owner'] = await TeamsDB.get_team_title(session=session, current_id=i['owner'])
            i['guest'] = await TeamsDB.get_team_title(session=session, current_id=i['guest'])
        if {i['status']} == 'Не начался':
            mes += f'\n { i['time']}: {i['owner']}  {i['scores']}  {i['guest']}'
        else:
            mes += f'\n {i['time']}: {i['owner']}  <tg-spoiler>{i['scores']}</tg-spoiler>  {i['guest']}'
        mes += f'\nСтатус матча: {i['status']}'
        mes += f'\n------------------------------'
    await message.answer(mes,parse_mode='HTML', reply_markup=kb.start)

@dp.message(F.text == 'Обновить данные')
async def upgrade_info(message: Message):
    logging.info(message.from_user.username)
    logging.info(message.from_user.id)
    await message.answer('Обновление началось...')
    async with httpx.AsyncClient() as client:
        await client.put('http://127.0.0.1:8000/upgradeDB')
    await message.answer('Обновление успешно завершено',reply_markup=kb.upgrade_info)


async def main():
    print("Бот запущен. Ожидаем задачи...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')