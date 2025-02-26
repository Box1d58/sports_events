from fastapi import APIRouter, HTTPException, status


from app.models_pydantic import TodayInfo, TodayEvent
from app.models_db import MatchDB
from app.database import async_session_maker


router_events = APIRouter()


@router_events.get("/events", response_model=TodayInfo)
async def events() -> dict:
        async with async_session_maker() as session:
            result = await MatchDB.get_today_events(session=session)
        return {"status": status.HTTP_200_OK, "today_events": result}
