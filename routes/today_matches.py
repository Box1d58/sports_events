from datetime import datetime
from bs4 import BeautifulSoup as BS
import requests
from main import app



current_date = datetime.now().strftime('%d.%m.%Y')
current_month = datetime.now().month


@app.get("/today_matches")
async def today_matches() -> dict:
    url_site = f"https://www.sports.ru/hockey/tournament/khl/calendar/?s=969354&m={current_month}"
    r = requests.get(url_site)
    html = BS(r.content, 'html.parser')
    print(current_date, ":")
    matches = {}
    c = 1
    for el in html.select(".stat-table > tbody > tr"):
        var_date = el.select(".name-td > a")
        match_date = var_date[0].text.strip()[:10]
        if match_date == current_date:
            owner = el.select(".owner-td > .rel > .player")
            guest = el.select(".guests-td > .rel > .player")
            score = el.select(".score-td > .score > noindex > b")
            matches[c] = f"{owner[0].text} {''.join([i.text for i in score])} {guest[0].text}"
            c += 1
    return matches