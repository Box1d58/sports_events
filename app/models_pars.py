from pydantic import BaseModel


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


class TodayEvent(BaseModel):
    match_info: MatchInfo
    owner: OwnerGuest
    guest: OwnerGuest


class TodayInfo(BaseModel):
    status: int
    today_events: list[TodayEvent]