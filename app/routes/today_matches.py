
from bs4 import BeautifulSoup as BS
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from httpx import AsyncClient

from app.config import settings
from app.models_pydantic import TodayInfo, TodayEvent
from app.parser import parser_today_matches
from app.models_db import MatchDB
from app.database import async_session_maker


router_add_matches = APIRouter()


@router_add_matches.post("/today_matches", response_model=TodayInfo)
async def today_matches() -> dict:
    current_date = datetime.now().strftime("%d.%m.%Y")
    current_month = datetime.now().month
    url_site = f"{settings.URL}{current_month}"

    async with AsyncClient() as client:
        response = await client.get(url_site)

    html = BS(response.content, "html.parser")
    try:
        matches = await parser_today_matches(current_date, html)
        for match in matches:
            match_instance = MatchDB(**match)
            async with async_session_maker() as session:
               await match_instance.create_match(match=match_instance, session=session)
        if not matches:
            raise ValueError("No items for parsing")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return {"status": status.HTTP_200_OK, "today_events": matches}