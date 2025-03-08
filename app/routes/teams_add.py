from fastapi import APIRouter, status

from app.database import async_session_maker
from app.models_db import TeamsDB

teams = [{'title':'Авангард'}, {'title':'Автомобилист'}, {'title':'Адмирал'},
         {'title':'Ак Барс'}, {'title':'Амур'}, {'title':'Барыс'}, {'title':'Витязь'},
         {'title':'Динамо Москва'}, {'title':'Динамо Минск'}, {'title':'Куньлунь'},
         {'title':'Лада'}, {'title':'Локомотив'}, {'title':'Металлург Мг'},
         {'title':'Нефтехимик'}, {'title':'СКА'}, {'title':'Салават Юлаев'},
         {'title':'Северсталь'}, {'title':'Сибирь'}, {'title':'Сочи'}, {'title':'Спартак'},
         {'title':'Торпедо'}, {'title':'Трактор'}, {'title':'ЦСКА'}]

router_team = APIRouter()

@router_team.post('/teams')
async def teams_add():
    for team in teams:
        team_instance = TeamsDB(**team)
        async with async_session_maker() as session:
            await team_instance.create_team(team=team_instance, session=session)
    return {'status': status.HTTP_200_OK}