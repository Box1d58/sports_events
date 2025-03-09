import requests

from bs4 import BeautifulSoup as BS

from app.database import async_session_maker
from app.models_db.teams import TeamsDB


async def parser_today_matches(current_date: str, html: BS) -> list:
    matches = []
    for el in html.select(".stat-table > tbody > tr"):
        date_info = el.select(".name-td > a")
        match_date = (
            date_info[0].text.strip().split("|")[0]
        )  # Получение даты матча из списка состоящего из даты и времени матча -> 1 элемент это время матча
        if match_date == current_date:
            owner = el.select(".owner-td > .rel > .player")[0].text
            guest = el.select(".guests-td > .rel > .player")[0].text
            url_for_status = el.select(".score-td > .score")[0].attrs["href"]
            response_url = requests.get(url_for_status)
            html_url = BS(response_url.content, "html.parser")
            match_status = html_url.select(
                ".match-summary__state > .match-summary__state-info > .match-summary__state-status"
            )[0].text
            if (
                len(
                    html_url.select(
                        ".match-summary__state > .match-summary__state-matchboard > .matchboard > span"
                    )
                )
                > 0
            ):
                owner_goal = int(
                    html_url.select(
                        ".match-summary__state > .match-summary__state-matchboard > .matchboard > span"
                    )[0].text[0]
                )
                guest_goal = int(
                    html_url.select(
                        ".match-summary__state > .match-summary__state-matchboard > .matchboard > span"
                    )[2].text[0]
                )
            else:
                owner_goal = "-"
                guest_goal = "-"
            scores = f'{owner_goal} : {guest_goal}'
            async with async_session_maker() as session:
                owner = await TeamsDB.get_team_id(session=session, current_team=owner)
                guest = await TeamsDB.get_team_id(session=session, current_team=guest)
            match = {
                "match_date": date_info[0].text.strip().split("|")[0],
                "time": date_info[0].text.strip().split("|")[1],
                "scores": scores,
                "owner": owner,
                "guest": guest,
                "status": match_status
            }
            matches.append(match)
    return matches
