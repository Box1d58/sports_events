import asyncio
import httpx
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime

from httpx import AsyncClient

import bot.keyboard as kb
from app.config import settings
from app.database import async_session_maker
from app.models_db.teams import TeamsDB
from app.models_db.follows import FollowDB

logging.basicConfig(level=logging.INFO)

current_date = datetime.now().strftime("%d.%m.%Y")
bot = Bot(settings.TOKEN)
dp = Dispatcher()

class SelectTeam(StatesGroup):
    id = State()

@dp.message(CommandStart())
async def start_bot(message: Message):
    logging.info(message.from_user.username)
    logging.info(message.from_user.id)
    async with async_session_maker() as session:
        await FollowDB.create_follow(new_user_id=message.from_user.id, follow=None, session=session)
    await message.reply("👋 Привет! Я твой помощник по КХЛ.\n"
            "📅 Я могу:\n"
            " Показывать сегодняшние матчи КХЛ\n"
            " Давать возможность выбрать любимую команду\n"
            " Отправлять уведомления в день игры\n\n"
            "🚀 Давай начнём! Нажми кнопку ниже, чтобы выбрать команду или посмотреть сегодняшние матчи."
                        , reply_markup=kb.upgrade_info)

@dp.message(F.text == 'Сегодняшние матчи')
async def events(message: Message):
    logging.info(message.from_user.username)
    logging.info(message.from_user.id)
    async with httpx.AsyncClient() as client:
        result = await client.get('http://127.0.0.1:8000/events')
    mes = f'📆 Сегодняшняя дата:{current_date}\n\n'
    #mes += f'------------------------------\n'
    for i in result.json().get('today_events'):
        async with async_session_maker() as session:
            i['owner'] = await TeamsDB.get_team_title(session=session, current_id=i['owner'])
            i['guest'] = await TeamsDB.get_team_title(session=session, current_id=i['guest'])
        if i['status'] == 'Не начался':
            mes += f'🏒 Матч: {i['owner']}  {i['scores']}  {i['guest']}\n'
        else:
            mes += f'🏒 Матч: {i['owner']}  <tg-spoiler>{i['scores']}</tg-spoiler> {i['guest']}\n'
        mes += f'🕔 Время: {i['time']}\n'
        mes += f'⏳ Статус: {i['status']}\n\n'
       # mes += f'\n------------------------------'
    await message.answer(mes,parse_mode='HTML', reply_markup=kb.upgrade)

@dp.message(F.text == 'Выбрать команду')
async def follow_1(message: Message, state: FSMContext):
    await state.set_state(SelectTeam.id)
    await message.answer('📋 Список доступных команд:\n\n')
    async with AsyncClient() as client:
        result = await client.get('http://127.0.0.1:8000/get_teams')
    mes = ''
    for i in result.json().get('teams'):
        mes += f'{i['id']}:  {i['title']} \n'
    await message.answer(mes)
    await message.answer('\n Введите номер команды, чтобы выбрать её.')

@dp.message(SelectTeam.id)
async def follow_2(message: Message, state: FSMContext):
    await state.update_data(id=int(message.text))
    follow_info = await state.get_data()
    if 1 > follow_info['id'] > 23:
        await message.answer('Вы ввели неверный номер, начните все сначала'
                             ,reply_markup=kb.upgrade_info)
    else:
        async with async_session_maker() as session:
            await FollowDB.update_follow(user_id=message.from_user.id,
                                         team_id=follow_info['id'],
                                         session=session)
            current_team = await TeamsDB.get_team_title(session=session, current_id=follow_info['id'])
        await message.answer(f'✅ Команда успешно выбрана: {current_team}\nТы будешь получать уведомления о её матчах.', reply_markup=kb.upgrade_info)
    await state.clear()

@dp.callback_query(F.data == 'upgrade_info')
async def upgrade_info(callback: CallbackQuery):
    logging.info(callback.message.from_user.username)
    logging.info(callback.message.from_user.id)
    await callback.message.answer('🔄 Начинаю обновление информации...')
    async with httpx.AsyncClient() as client:
        await client.put('http://127.0.0.1:8000/upgradeDB', timeout=100)
    await callback.message.answer('🎉 Успех! Данные обновлены.',reply_markup=kb.upgrade_info)
    await callback.answer()

async def send_message():
    async with AsyncClient() as client:
        result_follow = await client.get('http://127.0.0.1:8000/get_follow')
    async with AsyncClient() as client:
        result_events = await client.get('http://127.0.0.1:8000/check_follow')
    for i in result_follow.json().get('follows'):
        for j in result_events.json().get('today_events'):
            if i['follow_team'] == j['owner'] or i['follow_team'] == j['guest']:
                async with async_session_maker() as session:
                    i['follow_team'] = await TeamsDB.get_team_title(session=session, current_id=i['follow_team'])
                try:
                    await bot.send_message(i['user_id'], f"Сегодня в {j['time']} играет {i['follow_team']}")
                    continue
                except Exception as e:
                    logging.error(f'❌ Ошибка отправки сообщения пользователю {i['user_id']}')


async def main():
    print("Бот запущен. Ожидаем задачи...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')