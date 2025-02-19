import requests

from bs4 import BeautifulSoup as BS


def parser_today_matches(current_date: str, html: BS) -> list:
    matches = []
    for el in html.select(".stat-table > tbody > tr"):
        date_info = el.select(".name-td > a")
        match_date = (
            date_info[0].text.strip().split("|")[0]
        )  # Получение даты матча из списка состоящего из даты и времени матча -> 1 элемент это время матча
        if match_date == current_date:
            owner = el.select(".owner-td > .rel > .player")[0].text
            guest = el.select(".guests-td > .rel > .player")[0].text
            match = {
                "match_date": date_info[0].text.strip().split("|")[0],
                "owner": owner,
                "guest": guest
            }
            matches.append(match)
    return matches
