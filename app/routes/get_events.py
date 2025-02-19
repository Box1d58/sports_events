from bs4 import BeautifulSoup as BS
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from httpx import AsyncClient

from app.config import settings
from app.models_pydantic import TodayInfo, TodayEvent
from app.parser import parser_today_matches
from app.models_db import MatchDB
from app.database import async_session_maker


router_1 = APIRouter()


@router_1.get("/events", response_model=TodayInfo)
async def events() -> dict:
        async with async_session_maker() as session:
            result = await MatchDB.get_today_events(session=session)
        return {"status": status.HTTP_200_OK, "today_events": result}