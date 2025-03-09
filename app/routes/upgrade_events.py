import httpx

from fastapi import APIRouter, HTTPException, status

from app.models_pydantic import TodayInfo, TodayEvent
from app.models_db.matches import MatchDB
from app.database import async_session_maker



router_upgrade = APIRouter()

@router_upgrade.put("/upgradeDB")
async def update_current_events():
    async with httpx.AsyncClient() as client:
        result = await client.get('http://127.0.0.1:8000/get_today_matches',
                                  timeout=100
                                  )
        new_matches = result.json().get('today_events')
    async with async_session_maker() as session:
        await MatchDB.upgrade_match(session=session, new_matches=new_matches)
    return {'status': status.HTTP_200_OK}


