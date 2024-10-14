from pydantic import BaseModel


class TodayInfo(BaseModel):
    status: int
    date: str
    today_events: dict[str, list] = dict()