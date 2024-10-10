from bs4 import BeautifulSoup as BS
import requests

r = requests.get("https://www.sports.ru/hockey/tournament/khl/calendar/")
html = BS(r.content, 'html.parser')

for el in html.select(".stat-table > tbody > tr"):
    owner = el.select(".owner-td > .rel > .player")
    guest = el.select(".guests-td > .rel > .player")
    score = el.select(".score-td > .score > noindex > b")
    print(f"{owner[0].text} {''.join([i.text for i in score])} {guest[0].text}")