import requests


from datetime import datetime
from bs4 import BeautifulSoup as BS
from fastapi import APIRouter, status


from app.parser import parser_today_matches
from app.models_pars import TodayInfo


router = APIRouter()


@router.get("/today_matches", response_model=TodayInfo)
async def today_matches() -> dict:
    current_date = datetime.now().strftime("%d.%m.%Y")
    current_month = datetime.now().month
    url_site = f"https://www.sports.ru/hockey/tournament/khl/calendar/?s=969354&m={current_month}"
    r = requests.get(url_site)
    html = BS(r.content, "html.parser")
    matches = parser_today_matches(current_date, html)
    return {"status": status.HTTP_200_OK, "today_events": matches}