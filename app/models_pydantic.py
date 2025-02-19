from pydantic import BaseModel

class Match(BaseModel):
    match_date: str
    owner: str
    guest: str

class GoalInfo(BaseModel):
    goal_time: str
    player: str


class OwnerGuest(BaseModel):
    team: str
    score: int | str
    players: list[GoalInfo]


class MatchInfo(BaseModel):
    time: str
    date: str
    status: str


# class TodayEvent(BaseModel):
#     match_date: MatchInfo
#     owner: OwnerGuest
#     guest: OwnerGuest

class TodayEvent(BaseModel):
    match_date: str
    owner: str
    guest: str

class TodayInfo(BaseModel):
    status: int
    today_events: list[TodayEvent]