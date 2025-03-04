from pydantic import BaseModel

class Match(BaseModel):
    match_date: str
    time: str
    scores: str
    owner: int
    guest: int
    status: str

class Team(BaseModel):
    title: str

class User(BaseModel):
    nickname: str
    follow_team: int

class TodayEvent(BaseModel):
    match_date: str
    time: str
    scores: str
    owner: int
    guest: int
    status: str

class TodayInfo(BaseModel):
    status: int
    today_events: list[TodayEvent]