import requests


from bs4 import BeautifulSoup as BS


def parser_today_matches(current_date: str, html: BS) -> dict:
    matches = {}
    for el in html.select(".stat-table > tbody > tr"):
        var_date = el.select(".name-td > a")
        match_date = var_date[0].text.strip().split("|")[0] #Получение даты матча из списка состоящего из даты и времени матча -> 1 элемент это время матча
        if match_date == current_date:
            owner = el.select(".owner-td > .rel > .player")
            guest = el.select(".guests-td > .rel > .player")
            score = el.select(".score-td > .score > noindex > b")
            url_for_status = el.select(".score-td > .score")[0].attrs["href"]
            r_url = requests.get(url_for_status)
            html_url = BS(r_url.content, 'html.parser')
            match_status = html_url.select(".match-summary__state > .match-summary__state-info > .match-summary__state-status")[0].text
            players = []
            for i in html_url.select(".match-summary__goals--mobile > ul > li"):
                goal_time = i.select(".match-summary__score-info > span")[0].text
                player = i.select(".match-summary__score-info > span")[1].text
                players.append(f"{goal_time} {player}")
            matches[f"{var_date[0].text.strip().split("|")[1]}:({match_status}) {owner[0].text} {''.join([i.text for i in score])} {guest[0].text}"] = goalers
    return matches