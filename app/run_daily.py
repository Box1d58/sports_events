import httpx


async def run_daily():
    async with httpx.AsyncClient() as client:
        await client.get('http://127.0.0.1:8000/today_matches')