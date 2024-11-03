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
            url_for_status = el.select(".score-td > .score")[0].attrs["href"]
            r_url = requests.get(url_for_status)
            html_url = BS(r_url.content, "html.parser")
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
                    )[0].text
                )
                guest_goal = int(
                    html_url.select(
                        ".match-summary__state > .match-summary__state-matchboard > .matchboard > span"
                    )[2].text
                )
            else:
                owner_goal = "-"
                guest_goal = "-"
            owner_players = []
            guest_players = []
            for i in html_url.select(".match-summary__goals--mobile > ul > li"):
                goal_info = {}
                goal_time = i.select(".match-summary__score-info > span")[0].text
                player = i.select(".match-summary__score-info > span")[1].text
                if len(owner_players) == int(owner_goal):
                    goal_info["goal_time"] = goal_time
                    goal_info["player"] = player
                    guest_players.append(goal_info)
                else:
                    goal_info["goal_time"] = goal_time
                    goal_info["player"] = player
                    owner_players.append(goal_info)
            match = dict(
                match_info={
                    "time": date_info[0].text.strip().split("|")[1],
                    "date": date_info[0].text.strip().split("|")[0],
                    "status": match_status,
                },
                owner={
                    "team": owner,
                    "score": owner_goal,
                    "players": owner_players
                },
                guest={
                    "team": guest,
                    "score": guest_goal,
                    "players": guest_players
                }
            )
            matches.append(match)
    return matches
